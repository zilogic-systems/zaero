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
    PacketSniffer is a Robot Framework test library designed for  wireless sniffing automation.
    Provides monitor mode control, remote sniffing, and .pcap file fetching.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.log("PacketSniffer __init__ : START")
        DatabaseModule.__init__(self)
        UtilsModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("PacketSniffer __init__ : END")


    @keyword("Get Interface")
    def __get_interface(self,
                    device: str) -> str:
        zi_logger.log(f"lib.map.packetsniffer.__get_interface({device}")
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj= utils_obj.__get_interface(device)
        return utils_obj

    @keyword("Check Monitor Mode")
    def check_monitor_mode(self,
                        device: str,
                        interface: str):

        zi_logger.log(f"lib.map.packetsniffer.check_monitor_mode({device},{interface})")
        utils_obj = self.get_utils_module_object('sniffer')
        mode = utils_obj._PacketSniffer__check_monitor_mode(device, interface)
        return mode


    @keyword("Enable Monitor Mode")
    def enable_monitor_mode(self,
                            device: str):
        """
        Set the wireless interface to monitor mode.

        - ``device`` is the name given to the sniffer as mentioned
                     in the testbed.yaml config file

        Example:
        | Set Monitor Mode | sniffer |
        """
        zi_logger.log(f"lib.map.packetsniffer.enable_monitor_mode({device}")
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.enable_monitor_mode(device)

    @keyword("Disable Monitor Mode")
    def disable_monitor_mode(self,
                         device: str):
        zi_logger.log(f"lib.map.packetsniffer.disable_monitor_mode({device}")
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.disable_monitor_mode(device)

    @keyword("Lock Monitor Channel")
    def lock_monitor_channel(self,
                         device: str,
                         channel: int,
                         bandwidth: str) -> bool:

        zi_logger.log(f"lib.map.packetsniffer.lock_monitor_channel({device},{channel},{bandwidth}")
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.lock_monitor_channel(device,channel,bandwidth)

    @keyword("Set Sniffer Log Location")
    def set_sniffer_log_location(self,
                             device: str,
                             path: str) -> bool:
        zi_logger.log(f"lib.map.packetsniffer.set_sniffer_log_location({device},{path}")
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.set_sniffer_log_location(device,path)

    @keyword("Set Sniffer Log File")
    def set_sniffer_log_file(self,
                         device: str,
                         filename: str) -> bool:
        zi_logger.log(f"lib.map.packetsniffer.set_sniffer_log_file({device},{filename}")
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.set_sniffer_log_file(device,filename)

    @keyword("Start Frame Capture")
    def start_frame_capture(self,
                            device: str,
                            interface: str = None,
                            filter_expr: str = None,
                            timeout: int = None) -> bool:

        zi_logger.log(f"lib.map.packetsniffer.start_frame_capture({device},{timeout},{filter_expr})")
        utils_obj = self.get_utils_module_object('sniffer')
        result = utils_obj.start_frame_capture(device, interface, filter_expr, timeout)
        return result

    @keyword("Stop Frame Capture")
    def stop_frame_capture(self,
                       device: str) -> bool:
        zi_logger.log(f"lib.map.packetsniffer.stop_frame_capture({device}")
        utils_obj = self.get_utils_module_object('sniffer')
        utils_obj.stop_frame_capture(device)

    @keyword("Download Pcap")
    def download_pcap(self,
                  device: str,
                  remote_path: str = None,
                  local_path: str = None) -> str:
        zi_logger.log(f"lib.map.packetsniffer.download_pcap({device},{remote_path},{local_path}")
        utils_obj = self.get_utils_module_object('sniffer')
        file = utils_obj.download_pcap(device,remote_path,local_path)
        return file

    @keyword("List Captured Pcap")
    def list_captured_pcap(self, device : str):

        zi_logger.log(f"lib.map.packetsniffer.list_captured_pcap({device}")
        utils_obj = self.get_utils_module_object('sniffer')
        files = utils_obj.list_captured_pcap(device)
        return files

    @keyword("Check Monitor Channel")
    def __check_monitor_channel(self,
                            device: str,
                            interface: str) -> str:
        zi_logger.log(f"lib.map.packetsniffer.__check_monitor_channel({device},{interface}")
        utils_obj = self.get_utils_module_object('sniffer')
        files = utils_obj.__check_monitor_channel(device,interface)
        return files

    @keyword("Check Monitor Bandwidth")
    def __check_monitor_bandwidth(self,
                                  device : str,
                                  interface: str) -> str:
        zi_logger.log(f"lib.map.packetsniffer.__check_monitor_bandwidth({device},{interface}")
        utils_obj = self.get_utils_module_object('sniffer')
        files = utils_obj.__check_monitor_bandwidth(device,interface)
        return files


