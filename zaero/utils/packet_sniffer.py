# Copyright 2026 Zilogic Systems
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Author: Zilogic Systems <code@zilogic.com>
"""
import os
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
    """
    A library to sniff WiFi frames on a remote sniffer device. Handles
    monitor mode, channel locking, tcpdump sessions and fetching the
    .pcapng files.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        self.log_directory = "logs"
        self.log_directory_path = os.path.join('/root', self.log_directory)
        self.log_filename = None
        self.log_file_path = None
        self.pid = None
        zi_logger.log("Utils.FeaturePacketSniffer __init__ : END")

    def __kill_conflict_process(self,device:str):
        """
        Unblock the radios and kill the processes that interfere with monitor
        mode (``airmon-ng check kill``).

        ``device`` is the reference name of the sniffer
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        command = ("rfkill unblock all")
        output, error = connection_obj.execute_command(device, command, return_stderr=True)

        command= ("airmon-ng check kill")
        output, error = connection_obj.execute_command(device, command, return_stderr=True)

    def __check_monitor_mode(self,
                             device: str,
                             interface: str) -> bool:
        """
        Get the current mode of the wireless interface.

        ``device`` is the reference name of the sniffer
        and ``interface`` is the wireless interface, or None to detect it

        ``returns`` the interface type, e.g. monitor or managed

        ``raise`` RuntimeError if the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        if not interface:
            interface = self.__get_interface(device)

        command = f"iw dev {interface} info | grep 'type' | awk '{{print $2}}'"
        output, error = connection_obj.execute_command(device, command, return_stderr=True)

        if error != '':
            raise RuntimeError(f"Command execution failed : {command}")

        mode = output.strip()
        zi_logger.log(f"MODE: {mode}")

        return mode

    def __get_interface(self,
                        device: str) -> str:
        """
        Get the wireless interface name of the sniffer from ``iw dev``.

        ``device`` is the reference name of the sniffer

        ``returns`` the wireless interface name

        ``raise`` RuntimeError if no interface is found
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        command = "iw dev | grep 'Interface' | awk '{print $2}'"
        zi_logger.log(f"COMMAND: {command}")

        output, error = connection_obj.execute_command(device, command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        iface = output.strip()

        if not iface:
            raise RuntimeError("Interface not found")

        return iface

    def enable_monitor_mode(self,
                            device: str) -> bool:
        """
        Put the wireless interface into monitor mode with ``airmon-ng``,
        if it is not already in monitor mode.

        ``device`` is the reference name of the sniffer

        ``returns`` True if the interface is in monitor mode

        ``raise`` RuntimeError if the interface is not found or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        try:
            self.__kill_conflict_process(device)
            interface = self.__get_interface(device)

        except Exception as err:  # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not find interface for device: {device}")

        mode = self.__check_monitor_mode(device, interface)

        if mode != "monitor":
            command = f"airmon-ng start {interface}"
            zi_logger.log(f"COMMAND: {command}")

            _, error = connection_obj.execute_command(device, command, return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}")

        return True

    def disable_monitor_mode(self,
                             device: str):
        """
        Take the wireless interface out of monitor mode with ``airmon-ng``,
        if it is in monitor mode.

        ``device`` is the reference name of the sniffer

        ``raise`` RuntimeError if the interface is not found or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not find out the interface of the device : {device}")
        mode = self.__check_monitor_mode(device, interface)
        if mode == "monitor":
            command = f"airmon-ng stop {interface}"
            zi_logger.log(f"COMMAND: {command}")

            _, error = connection_obj.execute_command(device, command, return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}")

    def lock_monitor_channel(self,
                             device: str,
                             channel: int,
                             bandwidth: str) -> bool:
        """
        Set the monitor interface to the given channel and bandwidth and
        verify it.

        ``device`` is the reference name of the sniffer
        and ``channel`` is the channel number
        and ``bandwidth`` is the channel width as accepted by ``iw``, e.g. HT20, 80MHz

        ``returns`` True if the channel and bandwidth are set

        ``raise`` RuntimeError if the command fails or the values do not match
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not find out the interface of the device : {device}")
        command = f"iw dev {interface} set channel {channel} {bandwidth}"
        zi_logger.log(f"COMMAND: {command}")
        _, error = connection_obj.execute_command(device, command, return_stderr=True)
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
        """
        Get the current channel of the monitor interface.

        ``device`` is the reference name of the sniffer
        and ``interface`` is the monitor interface, or None to detect it

        ``returns`` the channel number as a string

        ``raise`` RuntimeError if the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        try:
            if not interface:
                interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not find interface for device : {device}")
        command = f"iw dev {interface} info | grep 'channel' | awk '{{print $2}}'"
        zi_logger.log(f"COMMAND: {command}")
        output, error = connection_obj.execute_command(device, command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")
        return output.strip()

    def __check_monitor_bandwidth(self,
                                  device : str,
                                  interface: str) -> str:
        """
        Get the current channel width of the monitor interface.

        ``device`` is the reference name of the sniffer
        and ``interface`` is ignored; the interface is always detected

        ``returns`` the channel width as a string
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not find interface for device : {device}")
        command = f"iw dev {interface} info | grep 'width' | awk " + "'{print $6}'"
        output, error = connection_obj.execute_command(device, command, return_stderr=True)
        return output.strip()

    def __get_remote_home(self,
                          device: str) -> str:
        """
        Get the home directory of the user logged into the sniffer.

        ``device`` is the reference name of the sniffer

        ``returns`` the home directory path
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        try:
            interface = self.__get_interface(device)
        except Exception as err:  # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not find interface for device : {device}")
        command = ("echo $HOME")
        output, error = connection_obj.execute_command(device, command, return_stderr=True)
        return output.strip()

    def set_sniffer_log_location(self,
                             device: str,
                             path: str) -> bool:
        """
        Set the directory, relative to the home directory of the sniffer, where
        the sniffed files are stored, and create it.

        ``device`` is the reference name of the sniffer
        and ``path`` is the directory relative to the home directory

        ``returns`` True if the directory is created

        ``raise`` RuntimeError if the directory could not be created
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        try:
            remote_home = self.__get_remote_home(device)
            self.log_directory = path
            self.log_directory_path = os.path.join(remote_home, self.log_directory)

        except Exception as err:
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not set log location for device: {device}")

        command = f"mkdir -p {self.log_directory_path}"
        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(device, command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        return True

    def set_sniffer_log_file(self,
                             device: str,
                             filename: str) -> bool:
        """
        Set the base file name for the next sniffing session and make sure the
        log directory exists.

        ``device`` is the reference name of the sniffer
        and ``filename`` is the file name without the .pcapng extension

        ``returns`` True if the file name is set

        ``raise`` RuntimeError if the file name is empty or the directory
        could not be created
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        try:
            if not filename:
                raise RuntimeError("Invalid filename")

            self.log_filename = filename


            if not hasattr(self, "log_directory_path") or not self.log_directory_path:
                remote_home = self.__get_remote_home(device)
                self.log_directory_path = os.path.join(remote_home, self.log_directory)

            command = f"mkdir -p {self.log_directory_path}"
            zi_logger.log(f"COMMAND: {command}")

            _, error = connection_obj.execute_command(device, command, return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}")

        except Exception as err:
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not set log file for device: {device}")

        zi_logger.log(f"Set Log Filename: {self.log_filename}")

        return True

    def __create_log_directory(self,
                               device: str):
        """
        Create the log directory under the home directory of the sniffer.

        ``device`` is the reference name of the sniffer

        ``returns`` the log directory path

        ``raise`` RuntimeError if the directory could not be created
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        try:
            self.remote_home = self.__get_remote_home(device)
            self.log_directory_path = os.path.join(self.remote_home, self.log_directory)
        except Exception as err:  # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Could not find remote home for device : {device}")
        command  = (f"mkdir -p {self.log_directory_path}")
        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(device, command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")
        return self.log_directory_path

    def start_frame_sniffing(self,
                             device: str,
                             interface: str = None,
                             filter_expr: str = None,
                             timeout: int = None) -> bool:
        """
        Start a tcpdump capture in the background on the sniffer. The file is
        named after the log file set earlier, or ``zisniff-<timestamp>``.

        ``device`` is the reference name of the sniffer
        and ``interface`` is the interface to sniff on, or None to detect it
        and ``filter_expr`` is the tcpdump filter expression, or None
        and ``timeout`` if given, rotates the capture file every ``timeout`` seconds

        ``returns`` True if the sniffing is started

        ``raise`` RuntimeError if the capture could not be prepared or started
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        try:
            self.__create_log_directory(device)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base = self.log_filename if self.log_filename else f"{DEFAULT_LOG_FILENAME}-{timestamp}"
            filename = f"{base}.pcapng"

            self.log_file_path = os.path.join(self.log_directory_path, filename)
            interface = interface or self.__get_interface(device)

        except Exception as err:
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(f"Failed to prepare capture on device: {device}")

        filter_part = f' "{filter_expr}"' if filter_expr else ""

        if timeout:
            command = f"nohup tcpdump -i {interface} -G {timeout} -w {self.log_file_path} -e {filter_part} {BG}"
        else:
            command = f"nohup tcpdump -i {interface} -w {self.log_file_path} -e {filter_part} {BG}"

        zi_logger.log(f"COMMAND: {command}")

        _, error = connection_obj.execute_command(device, command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        return True

    def stop_frame_sniffing(self,
                            device: str) -> bool:
        """
        Stop the tcpdump capture on the sniffer. Kills the recorded process if
        known, otherwise all tcpdump processes.

        ``device`` is the reference name of the sniffer

        ``returns`` True if stopped, or no tcpdump was running

        ``raise`` RuntimeError if tcpdump could not be stopped
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        if not self.pid:
            _, error = connection_obj.execute_command(device, "killall tcpdump", return_stderr=True)
            if error != '' and "tcpdump: no process killed" not in error:
                raise RuntimeError(f"Command execution failed: killall tcpdump")
            return True
        command = f"kill -9 {self.pid}"
        zi_logger.log(f"COMMAND: {command}")
        _, error = connection_obj.execute_command(device, command, return_stderr=True)

        if error:
            raise RuntimeError(f"Command execution failed: {command}")

        self.pid = None
        return True


    def delete_sniffed_pcap(self,
                            device: str,
                            pcap_file=None):
        """
        Delete a sniffed file from the log directory of the sniffer.

        ``device`` is the reference name of the sniffer
        and ``pcap_file`` is the file name in the log directory

        ``raise`` ValueError if no file name is given and RuntimeError if the
        file could not be deleted
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        remote_path = None

        if pcap_file:
            remote_path = os.path.join(self.log_directory_path, pcap_file)
        else:
            raise ValueError("No pcap file name specified")

        zi_logger.log(f"Remote path: {remote_path}")
        _, error = connection_obj.execute_command(device, f"rm {remote_path}", return_stderr=True)
        if error:
            raise RuntimeError(f"Failed to delete: {remote_path}")


    def download_sniffed_pcap(self,
                              device: str,
                              remote_path: str = None,
                              local_path: str = None) -> str:
        """
        Copy a sniffed file from the sniffer to the local machine.

        ``device`` is the reference name of the sniffer
        and ``remote_path`` is the file name in the log directory, or None for
        the file of the last sniffing session
        and ``local_path`` is the local file or directory, or None for the
        home directory

        ``returns`` the local path of the copied file

        ``raise`` RuntimeError if there is no file to download
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

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

        connection_obj.get_file(device, remote_path, local_file)

        return local_file

    def list_sniffed_pcap(self,
                          device: str):
        """
        List the .pcapng files in the log directory of the sniffer.

        ``device`` is the reference name of the sniffer

        ``returns`` the list of file names, empty if there are none

        ``raise`` RuntimeError if the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        if not hasattr(self, 'log_directory_path') or not self.log_directory_path:
            return []

        command = f"ls {self.log_directory_path} | grep '.pcapng'"
        output, error = connection_obj.execute_command(device, command, return_stderr=True)
        if error:
            raise RuntimeError(f"Command execution failed: {command}")
        if not output:
            return []
        return output.strip().splitlines()


