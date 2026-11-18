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
Robot Framework keywords to capture packets with tcpdump on a device.

Author: Zilogic Systems <code@zilogic.com>
"""


from robot.api.deco import keyword

from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.utils_modules import UtilsModules
import zaero.utils.zi_logger as zi_logger
from typing import Optional, List, Dict

class PacketCapture(DatabaseModule,
                    UtilsModules):
    """
    Keywords to capture packets with tcpdump on a device and fetch the
    capture files. Files are written to the ``pcap_remote_dir`` of the
    device and copied into its ``pcap_local_dir``.
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

    @keyword("Start Frame Capture")
    def start_frame_capture(self,
                            device: str,
                            interface: str = None,
                            filter_expr: str = None,
                            filename: str = None,
                            timeout: int = None) -> bool:
        """
        Start a tcpdump capture in the background on the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the interface to capture on

        - ``filter_expr`` is the tcpdump filter expression, or None for no filter

        - ``filename`` is the capture file name, created in ``pcap_remote_dir``

        - ``timeout`` if given, tcpdump starts a new file every ``timeout``
          seconds (``-G``)

        - ``Returns`` True if the capture is started

        - ``Raises`` RuntimeError if a command fails

        Example:
        | Start Frame Capture | controller | br-lan | icmp | ping.pcap |
        | Start Frame Capture | controller | br-lan | ${None} | all.pcap | timeout=60 |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('capture')
        result = utils_obj.start_frame_capture(device, interface, filter_expr, filename, timeout)
        return result

    @keyword("Stop Frame Capture")
    def stop_frame_capture(self,
                           device: str) -> bool:
        """
        Stop all running tcpdump processes on the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` RuntimeError if tcpdump could not be stopped

        Example:
        | Stop Frame Capture | controller |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('capture')
        utils_obj.stop_frame_capture(device)

    @keyword("Download Captured Pcap")
    def download_captured_pcap(self,
                               device: str,
                               filename: str = None) -> str:
        """
        Copy a capture file from ``pcap_remote_dir`` of the device to its
        ``pcap_local_dir``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``filename`` is the capture file name

        - ``Returns`` the local path of the copied file

        - ``Raises`` Exception if the file was not copied

        Example:
        | ${file} | Download Captured Pcap | controller | ping.pcap |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('capture')
        file = utils_obj.download_captured_pcap(device, filename)
        return file

    @keyword("Delete Captured Pcap")
    def delete_captured_pcap(self,
                             device: str ,
                             filename=None):
        """
        Delete a capture file from ``pcap_remote_dir`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``filename`` is the capture file name

        - ``Raises`` ValueError if no file name is given, RuntimeError if the
          file could not be deleted

        Example:
        | Delete Captured Pcap | controller | ping.pcap |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('capture')
        files = utils_obj.delete_captured_pcap(device, filename)
