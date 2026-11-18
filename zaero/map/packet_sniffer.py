# Copyright 2025 Zilogic Systems
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
Robot Framework keywords for WiFi sniffing on a sniffer device.

Author: Zilogic Systems <code@zilogic.com>
"""


from robot.api.deco import keyword

from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.utils_modules import UtilsModules
import zaero.utils.zi_logger as zi_logger
from typing import Optional, List, Dict

class PacketSniffer(DatabaseModule,
                    UtilsModules):
    """
    Keywords to sniff WiFi frames on a sniffer device: monitor mode control,
    channel locking, tcpdump sessions and fetching the .pcapng files.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        UtilsModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("PacketSniffer __init__ : END")


    @keyword("Get Interface")
    def get_interface(self,
                      device: str) -> str:
        """
        Get the wireless interface name of the sniffer (first interface listed
        by ``iw dev``).

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``Returns`` the interface name

        - ``Raises`` RuntimeError if no interface is found

        Example:
        | ${iface} | Get Interface | sniffer |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj= utils_obj.__get_interface(device)
        return utils_obj

    @keyword("Check Monitor Mode")
    def check_monitor_mode(self,
                           device: str,
                           interface: str):
        """
        Get the current mode of the wireless interface.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``interface`` is the wireless interface, or None to detect it

        - ``Returns`` the interface type, e.g. ``monitor`` or ``managed``

        - ``Raises`` RuntimeError if the command fails

        Example:
        | ${mode} | Check Monitor Mode | sniffer | wlan0mon |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        mode = utils_obj._PacketSniffer__check_monitor_mode(device, interface)
        return mode


    @keyword("Enable Monitor Mode")
    def enable_monitor_mode(self,
                            device: str):
        """
        Put the wireless interface into monitor mode with ``airmon-ng``.

        Unblocks the radios and stops processes that interfere with monitor
        mode first. Does nothing if the interface is already in monitor mode.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``Raises`` RuntimeError if the interface is not found or the command
          fails

        Example:
        | Enable Monitor Mode | sniffer |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.enable_monitor_mode(device)

    @keyword("Disable Monitor Mode")
    def disable_monitor_mode(self,
                             device: str):
        """
        Take the wireless interface out of monitor mode with ``airmon-ng``.
        Does nothing if the interface is not in monitor mode.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``Raises`` RuntimeError if the interface is not found or the command
          fails

        Example:
        | Disable Monitor Mode | sniffer |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.disable_monitor_mode(device)

    @keyword("Lock Monitor Channel")
    def lock_monitor_channel(self,
                             device: str,
                             channel: int,
                             bandwidth: str) -> bool:
        """
        Set the monitor interface to the given channel and bandwidth and verify
        it.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``channel`` is the channel number

        - ``bandwidth`` is the channel width as accepted by ``iw``,
          e.g. ``HT20`` or ``80MHz``

        - ``Raises`` RuntimeError if the command fails or the channel and
          bandwidth do not match afterwards

        Example:
        | Lock Monitor Channel | sniffer | 36 | 80MHz |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.lock_monitor_channel(device, channel, bandwidth)

    @keyword("Set Sniffer Log Location")
    def set_sniffer_log_location(self,
                                 device: str,
                                 path: str) -> bool:
        """
        Set the directory, relative to the home directory of the sniffer, where
        the sniffed files are stored, and create it.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``path`` is the directory relative to the home directory

        - ``Raises`` RuntimeError if the directory could not be created

        Example:
        | Set Sniffer Log Location | sniffer | logs/TC001 |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.set_sniffer_log_location(device, path)

    @keyword("Set Sniffer Log File")
    def set_sniffer_log_file(self,
                             device: str,
                             filename: str) -> bool:
        """
        Set the file name for the next sniffing session.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``filename`` is the file name without the ``.pcapng`` extension

        - ``Raises`` RuntimeError if the file name is empty or the log directory
          could not be created

        Example:
        | Set Sniffer Log File | sniffer | TC001 |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.set_sniffer_log_file(device, filename)

    @keyword("Start Frame Sniffing")
    def start_frame_sniffing(self,
                             device: str,
                             interface: str = None,
                             filter_expr: str = None,
                             timeout: int = None) -> bool:
        """
        Start a tcpdump capture in the background on the sniffer.

        The file is named after `Set Sniffer Log File`, or
        ``zisniff-<timestamp>.pcapng`` if no name was set.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``interface`` is the interface to sniff on, or None to detect it

        - ``filter_expr`` is the tcpdump filter expression, or None

        - ``timeout`` if given, tcpdump starts a new file every ``timeout``
          seconds (``-G``)

        - ``Returns`` True if sniffing is started

        - ``Raises`` RuntimeError if the capture could not be prepared or started

        Example:
        | Start Frame Sniffing | sniffer |
        | Start Frame Sniffing | sniffer | wlan0mon | type mgt subtype beacon |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        result = utils_obj.start_frame_sniffing(device, interface, filter_expr, timeout)
        return result

    @keyword("Stop Frame Sniffing")
    def stop_frame_Sniffing(self,
                            device: str) -> bool:
        """
        Stop the tcpdump capture on the sniffer.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``Raises`` RuntimeError if tcpdump could not be stopped

        Example:
        | Stop Frame Sniffing | sniffer |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.stop_frame_sniffing(device)

    @keyword("Download Sniffed Pcap")
    def download_sniffed_pcap(self,
                              device: str,
                              remote_path: str = None,
                              local_path: str = None) -> str:
        """
        Copy a sniffed file from the sniffer to the local machine.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``remote_path`` is the file name in the log directory, or None for
          the file of the last sniffing session

        - ``local_path`` is the local file or directory, or None for the home
          directory

        - ``Returns`` the local path of the copied file

        - ``Raises`` RuntimeError if there is no file to download

        Example:
        | ${file} | Download Sniffed Pcap | sniffer |
        | ${file} | Download Sniffed Pcap | sniffer | TC001.pcapng | /tmp |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        file = utils_obj.download_sniffed_pcap(device, remote_path, local_path)
        return file

    @keyword("List Sniffed Pcap")
    def list_sniffed_pcap(self, device : str):
        """
        List the ``.pcapng`` files in the log directory of the sniffer.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``Returns`` the list of file names, empty if there are none

        - ``Raises`` RuntimeError if the command fails

        Example:
        | ${files} | List Sniffed Pcap | sniffer |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        files = utils_obj.list_sniffed_pcap(device)
        return files

    @keyword("Check Monitor Channel")
    def check_monitor_channel(self,
                              device: str,
                              interface: str) -> str:
        """
        Get the current channel of the monitor interface.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``interface`` is the monitor interface, or None to detect it

        - ``Returns`` the channel number as a string

        - ``Raises`` RuntimeError if the command fails

        Example:
        | ${channel} | Check Monitor Channel | sniffer | wlan0mon |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        files = utils_obj.__check_monitor_channel(device, interface)
        return files

    @keyword("Check Monitor Bandwidth")
    def check_monitor_bandwidth(self,
                                device : str,
                                interface: str) -> str:
        """
        Get the current channel width of the monitor interface.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``interface`` is not used; the interface is always detected

        - ``Returns`` the channel width as a string

        Example:
        | ${width} | Check Monitor Bandwidth | sniffer | wlan0mon |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        files = utils_obj.__check_monitor_bandwidth(device, interface)
        return files

    @keyword("Delete Sniffed Pcap")
    def delete_sniffed_pcap(self, device: str , remote_path=None):
        """
        Delete a sniffed file from the log directory of the sniffer.

        - ``device`` is the sniffer name as defined in the infra.yaml config file

        - ``remote_path`` is the file name in the log directory

        - ``Raises`` ValueError if no file name is given, RuntimeError if the
          file could not be deleted

        Example:
        | Delete Sniffed Pcap | sniffer | TC001.pcapng |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('sniffer')
        files = utils_obj.delete_sniffed_pcap(device, remote_path)

