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


# Third-party Libraries
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger
from zaero.bridge.utils_modules import UtilsModules
from zaero.bridge.connection_modules import ConnectionModules
from robot.api.deco import keyword

class TrafficGenerator(DatabaseModule,UtilsModules,ConnectionModules):
    """
    TrafficGenerator is a Robot Framework test library for
    performing iperf-based traffic generation over SSH.

    This library is designed to cover the full functionality of
    the iperf tool across different platforms.

    It provides multiple keywords that allow interaction with
    iperf through SSH connections.
    """
    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.log("Traffic_Generator __init__ : START")
        DatabaseModule.__init__(self)
        UtilsModules.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Traffic_generator __init__ : END")

    @keyword("Start Iperf Server")
    def start_iperf_server(self, # pylint: disable=R0913
                           device: str,
                           bind_ip: str,
                           log_name: str,
                           port: int = 5201):
        """
        Generate an iperf server and store logs locally.

        - ``device`` Specifies the device name.
        - ``bind_ip`` Specified associated with the address
        - ``log_name`` Name of the log file,
            typically set to the test case name.
        - ``port`` Specifies the port number. The default is 5201.

        Example:
        | Start Iperf Server  | Ap | 192.168.1.1 | demo |
        | Start Iperf Server  | Ap | 192.168.1.1 | log_name = TC001 | 5001 |
        | Start Iperf Server  | Ap | 192.168.1.1 | demo | port = 5222 |

        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.start_iperf_server({device}, "
            f"{bind_ip}, {log_name}, {port} ")
        utils_obj = self.get_utils_module_object('traffic_generator')
        utils_obj.start_iperf_server(device,
                                     bind_ip,
                                     log_name,
                                     port)

    @keyword("Start Iperf Client")
    def start_iperf_client(self,  # pylint: disable=R0913
                        device: str,
                        server_ip: str,
                        bind_ip: str,
                        protocol: str,
                        log_name: str,
                        port: int = 5201,
                        time: int = None,
                        bitrate: str = None,
                        tos: str = None,
                        window_size: str = None,
                        mode: str = None,
                        parallel_streams: int = None):
        """
        Start iperf3 client traffic.

        timeout: Duration of the iperf3 test in seconds.
        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.start_iperf_client("
            f"{device}, {server_ip}, {bind_ip}, {protocol}, "
            f"{log_name}, {port}, {time})"
        )

        utils_obj = self.get_utils_module_object('traffic_generator')

        utils_obj.start_iperf_client(
            device,
            server_ip,
            bind_ip,
            protocol,
            log_name,
            port,
            time,
            bitrate,
            tos,
            window_size,
            mode,
            parallel_streams
        )

    @keyword("Stop Iperf Server")
    def stop_iperf_server(self,
                          device: str):
        """
        Stop the iperf server using `pkill` on Linux/macOS
        or `taskkill` on Windows.

        - ``device``       Specifies the device name.

        Example:
        | Stop Iperf Server | Ap |
        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.stop_iperf_server({device})")
        utils_obj = self.get_utils_module_object('traffic_generator')
        utils_obj.stop_iperf_server(device)

    @keyword("Get Iperf Log")
    def get_iperf_log(self,
                      device: str,
                      remote_file: str,
                      local_file: str):
        """
        Retrieve a iperf log from the remote machine.

        - ``device`` Specified a remote device.
        - ``remote_file`` The file path on the remote machine.
        - ``local_file`` The destination path on the local.

        Example:
        | Get Iperf Log | Ap | /remote/file.log | /tmp/file.log | #Linux |
        | Get Iperf Log | Ap | C:\\remote\\file.log | C:\\file.log | #Windows |
        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.get_iperf_log({device},"  
            f"{remote_file}, {local_file})")        
        utils_obj = self.get_utils_module_object('traffic_generator')
        utils_obj.get_iperf_log(device, remote_file, local_file)

    @keyword("Put Iperf Log")
    def put_iperf_log(self,
                      device: str,
                      local_file: str,
                      remote_file: str):
        """
        Transfer a file from the local machine to the remote machine.

        - ``device`` Specified the remote machine.
        - ``local_file`` The file path on the local machine.
        - ``remote_file`` The destination path on the remote.

        Example:
        | Put Iperf Log | Ap | /test/file.log | /tmp/file.log | # Linux |
        | Put Iperf Log | Ap | C:\\local\\file.log | C:\\file.log | # Windows |
        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.put_iperf_log({device}, "  
            f"{local_file}, {remote_file}")
        utils_obj = self.get_utils_module_object('traffic_generator')
        utils_obj.put_iperf_log(device, local_file, remote_file)

    @keyword("Remove Iperf Logs")
    def remove_iperf_logs(self,
                          device: str,
                          dirpath: str):
        """
        Remove Iperf Logs From specified device and specified directory.

        - ``device`` Mention a device name.
        - ``dirpath`` Specified a directory path

        Example:
        | Remove Iperf Logs | Client | /tmp | # For Linux |
        | Remove Iperf Logs | Client | C:\\Windows\temp" | # Windows |
        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.remove_iperf_logs({device})")
        utils_obj = self.get_utils_module_object('traffic_generator')
        utils_obj.remove_iperf_logs(device, dirpath)

    @keyword("Remove Iperf Log")
    def remove_iperf_log(self,
                         device: str,
                         filename: str):
        """
        Remove Iperf Log From specified device.

        - ``device`` Mention a device name.
        - ``filename`` Specified filename.

        Example:
        | Remove Iperf Log | Client | /tmp/iperf.log |  # For Linux |
        | Remove Iperf Log | Client | C:\\temp\\iperf.log | # Windows |
        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.remove_iperf_log({device})")
        utils_obj = self.get_utils_module_object('traffic_generator')
        utils_obj.remove_iperf_log(device, filename)