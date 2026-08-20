import os
from pathlib import Path
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger

class PacketCapture(DatabaseModule,
                    ConnectionModules):    

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        self.log_directory = "~/capture_logs"
        self.log_filename = None
        self.log_file_path = None
        self.pid = None

    def start_frame_capture(self,
                            device: str,
                            interface: str,
                            filter_expr: str,
                            filename: str,
                            timeout: int):
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        remote_log_directory = self.db_obj.read_from_database(device, 'pcap_remote_dir')
        command  = (f"mkdir -p {remote_log_directory}")
        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        self.log_file = os.path.join(remote_log_directory, filename)

        filter_part = f' "{filter_expr}"' if filter_expr else ""
        BG = "> /tmp/bg_cmd.log 2>&1 < /dev/null & echo $!"

        if timeout:
            command = f"nohup tcpdump -i {interface} -G {timeout} -w {self.log_file} -e {filter_part} {BG}"
        else:
            command = f"nohup tcpdump -i {interface} -w {self.log_file} -e {filter_part} {BG}"

        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        return True

    def stop_frame_capture(self,
                           device):
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        try:
            _, error = connection_obj.execute_command("killall tcpdump", return_stderr=True)
            if error != '' and "tcpdump: no process killed" not in error:
                raise RuntimeError(f"Command execution failed: killall tcpdump")
            return True
        except Exception as E:
            raise RuntimeError(E)

    def delete_captured_pcap(self,
                             device: str,
                             pcap_file=None):
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        if pcap_file:
            remote_log_directory = self.db_obj.read_from_database(device, 'pcap_remote_dir')
            remote_path = os.path.join(remote_log_directory, pcap_file)
        else:
            raise ValueError("No pcap file name specified")

        zi_logger.log(f"Remote path: {remote_path}")
        _, error = connection_obj.execute_command(f"rm {remote_path}", return_stderr=True)
        if error:
            raise RuntimeError(f"Failed to delete: {remote_path}")


    def download_captured_pcap(self,
                               device: str,
                               file_name: str = None) -> str:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        remote_log_directory = self.db_obj.read_from_database(device, 'pcap_remote_dir')
        remote_path = os.path.join(remote_log_directory, file_name)
        if not remote_path:
            raise RuntimeError("No remote path specified")

        local_log_directory = self.db_obj.read_from_database(device, 'pcap_local_dir')
        local_file = os.path.join(local_log_directory, file_name)

        zi_logger.log(f"REMOTE: {remote_path}")
        zi_logger.log(f"LOCAL: {local_file}")

        connection_obj.get_file(remote_path, local_file)

        local_file = Path(local_file)
        
        if not local_file.exists():
            raise Exception(f"Captured file could not be copied : {str(local_file)}")

        return str(local_file)
