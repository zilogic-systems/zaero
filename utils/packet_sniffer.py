import os
import paramiko
import datetime
import time
from pathlib import Path
from typing import Optional, List, Dict
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger


LOCAL_LOG_PATH = str(Path.home())
DEFAULT_LOG_FILENAME = "zisniff"
BG = "> /tmp/bg_cmd.log 2>&1 < /dev/null & echo $!"

class PacketSniffer(DatabaseModule,
                        ConnectionModules):

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.log("Utils.FeaturePacketSniffer __init__ : START")
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        self.log_directory = "sniffer-logs"
        self.log_directory_path = os.path.join('/root', self.log_directory)
        self.log_filename = None
        self.log_file_path = None
        self.pid = None
        self.sftp = None
        self._hostname = None
        self._port     = None
        self._username = None
        self._password = None
        self._timeout  = None
        zi_logger.log("Utils.FeaturePacketSniffer __init__ : END")

    def __kill_conflict_process(self,device:str):

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        command = ("rfkill unblock all")
        output, error = connection_obj.execute_command(command, return_stderr=True)

        command= ("airmon-ng check kill")
        output, error = connection_obj.execute_command(command, return_stderr=True)

    def __check_monitor_mode(self,
                             device: str,
                             interface: str) -> bool:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        if not interface:
            interface = self.__get_interface(device)

        command = f"iw dev {interface} info | grep 'type' | awk '{{print $2}}'"
        output, error = connection_obj.execute_command(command, return_stderr=True)

        if error != '':
            raise RuntimeError(f"Command execution failed : {command}")

        mode = output.strip()
        zi_logger.log(f"MODE: {mode}")

        return mode

    def __get_interface(self,
                    device: str) -> str:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        command = "iw dev | grep 'Interface' | awk '{print $2}'"
        zi_logger.log(f"COMMAND: {command}")

        output, error = connection_obj.execute_command(command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        iface = output.strip()

        if not iface:
            raise RuntimeError("Interface not found")

        return iface

    def enable_monitor_mode(self,
                        device: str) -> bool:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        try:
            self.__kill_conflict_process(device)
            interface = self.__get_interface(device)

        except Exception as err:  # pylint: disable=broad-except
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not find interface for device: {device}")

        mode = self.__check_monitor_mode(device, interface)

        if mode != "monitor":
            command = f"airmon-ng start {interface}"
            zi_logger.log(f"COMMAND: {command}")

            _, error = connection_obj.execute_command(command, return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}")

        return True

    def disable_monitor_mode(self,
                         device: str):

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not find out the interface of the device : {device}")
        mode = self.__check_monitor_mode(device, interface)
        if mode == "monitor":
            command = f"airmon-ng stop {interface}"
            zi_logger.log(f"COMMAND: {command}")

            _, error = connection_obj.execute_command(command, return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}")

    def lock_monitor_channel(self,
                         device: str,
                         channel: int,
                         bandwidth: str) -> bool:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not find out the interface of the device : {device}")
        command = f"iw dev {interface} set channel {channel} {bandwidth}"
        zi_logger.log(f"COMMAND: {command}")
        _, error = connection_obj.execute_command(command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")
        current_channel = self.__check_monitor_channel(device, interface)
        current_bandwidth = self.__check_monitor_bandwidth(device, interface)
        zi_logger.log(f"CURRENT channel={current_channel}, bandwidth={current_bandwidth}")
        if int(current_channel) != channel or current_bandwidth not in bandwidth:
            raise RuntimeError("Lock monitor not matched to actual channel and bandwidth")
        return True

    def __check_monitor_channel(self,
                            device: str,
                            interface: str) -> str:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        try:
            if not interface:
                interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not find interface for device : {device}")
        command = f"iw dev {interface} info | grep 'channel' | awk '{{print $2}}'"
        zi_logger.log(f"COMMAND: {command}")
        output, error = connection_obj.execute_command(command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")
        return output.strip()

    def __check_monitor_bandwidth(self,
                                  device : str,
                                  interface: str) -> str:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not find interface for device : {device}")
        command = f"iw dev {interface} info | grep 'width' | awk " + "'{print $6}'"
        output, error = connection_obj.execute_command(command, return_stderr=True)
        return output.strip()

    def __get_remote_home(self,
                          device: str) -> str:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not find interface for device : {device}")
        command = ("echo $HOME")
        output, error = connection_obj.execute_command(command, return_stderr=True)
        return output.strip()

    def set_sniffer_log_location(self,
                             device: str,
                             path: str) -> bool:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        try:
            remote_home = self.__get_remote_home(device)
            self.log_directory = path
            self.log_directory_path = os.path.join(remote_home, self.log_directory)

        except Exception as err:
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not set log location for device: {device}")

        command = f"mkdir -p {self.log_directory_path}"
        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        return True

    def set_sniffer_log_file(self,
                             device: str,
                             filename: str) -> bool:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        try:
            if not filename:
                raise RuntimeError("Invalid filename")

            self.log_filename = filename


            if not hasattr(self, "log_directory_path") or not self.log_directory_path:
                remote_home = self.__get_remote_home(device)
                self.log_directory_path = os.path.join(remote_home, self.log_directory)

            command = f"mkdir -p {self.log_directory_path}"
            zi_logger.log(f"COMMAND: {command}")

            _, error = connection_obj.execute_command(command, return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}")

        except Exception as err:
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not set log file for device: {device}")

        zi_logger.log(f"Set Log Filename: {self.log_filename}")

        return True

    def __create_log_directory(self,
                               device: str):

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        try:
            self.remote_home = self.__get_remote_home(device)
            self.log_directory_path = os.path.join(self.remote_home, self.log_directory)
        except Exception as err:  # pylint: disable=broad-except
            print(f"ERROR: {err}")
            raise RuntimeError(f"Could not find remote home for device : {device}")
        command  = (f"mkdir -p {self.log_directory_path}")
        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")
        return self.log_directory_path

    def start_frame_capture(self,
                            device: str,
                            interface: str = None,
                            filter_expr: str = None,
                            timeout: int = None) -> bool:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        try:
            self.__create_log_directory(device)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base = self.log_filename if self.log_filename else f"{DEFAULT_LOG_FILENAME}-{timestamp}"
            filename = f"{base}.pcapng"

            self.log_file_path = os.path.join(self.log_directory_path, filename)
            interface = interface or self.__get_interface(device)

        except Exception as err:
            print(f"ERROR: {err}")
            raise RuntimeError(f"Failed to prepare capture on device: {device}")

        filter_part = f' "{filter_expr}"' if filter_expr else ""

        if timeout:
            command = f"nohup tcpdump -i {interface} -G {timeout} -w {self.log_file_path} -e {filter_part} {BG}"
        else:
            command = f"nohup tcpdump -i {interface} -w {self.log_file_path} -e {filter_part} {BG}"

        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        return True

    def stop_frame_capture(self,
                       device: str) -> bool:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        if not self.pid:
            _, error = connection_obj.execute_command("killall tcpdump", return_stderr=True)
            if error != '' and "tcpdump: no process killed" not in error:
                raise RuntimeError(f"Command execution failed: killall tcpdump")
            return True
        command = f"kill -9 {self.pid}"
        zi_logger.log(f"COMMAND: {command}")
        _, error = connection_obj.execute_command(command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        self.pid = None
        return True

    def __open_sftp(self, connection_obj):
        try:
            if self.sftp is None:
                self.sftp = connection_obj.open_sftp()
                zi_logger.log("SFTP connection opened")
        except Exception as e:
            raise RuntimeError(f"SFTP open failed: {e}")

    def __close_sftp(self):
        if self.sftp:
            self.sftp.close()
            self.sftp = None
            zi_logger.log("SFTP connection closed")

    def delete_pcap(self, remote_path=None):
        try:
            self.__open_sftp()
            if remote_path:
                remote_path = os.path.join(self.log_directory_path, remote_path)
            else:
                raise ValueError("No remote path specified")
            print(f"Remove path: {remote_path}")
            self.sftp.remove(remote_path)
        except Exception as e:
            raise Exception(f"SFTP download failed: {e}")
        finally:
            self.__close_sftp()


    def download_pcap(self,
                  device: str,
                  remote_path: str = None,
                  local_path: str = None) -> str:

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        try:
            self.__open_sftp(connection_obj)
            if remote_path:
                remote_path = os.path.join(self.log_directory_path, remote_path)
            else:
                remote_path = self.log_file_path

            if not remote_path:
                raise RuntimeError("No remote path specified")

            local_path = local_path or LOCAL_LOG_PATH
            filename = os.path.basename(remote_path)

            if os.path.isdir(local_path):
                local_file = os.path.join(local_path, filename)
            else:
                local_file = local_path

            zi_logger.log(f"REMOTE: {remote_path}")
            zi_logger.log(f"LOCAL: {local_file}")

            self.sftp.get(remote_path, local_file)

        except Exception as e:
            raise RuntimeError(f"SFTP download failed: {e}")

        finally:
            self.__close_sftp()

        return local_file

    def list_captured_pcap(self, device: str):

        zi_logger.log(f"lib.utils.packet_sniffer.({device})")

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        if not hasattr(self, 'log_directory_path') or not self.log_directory_path:
            return []

        command = f"ls {self.log_directory_path} | grep '.pcapng'"
        output, error = connection_obj.execute_command(command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")
        if not output:
            return []
        return output.strip().splitlines()


