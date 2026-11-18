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
Robot Framework keywords to generate traffic with iperf3.

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
    Keywords to run iperf3 servers and clients on devices and handle their
    log files. Commands are run through the device's connection.
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
        Start an iperf3 server in the background on the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``bind_ip`` is the address the server binds to (``-B``)

        - ``log_name`` is the log file on the device (``--logfile``),
          e.g. the test case name

        - ``port`` is the server port (``-p``). Defaults to 5201

        Example:
        | Start Iperf Server | controller | 192.168.1.1 | TC001.log |
        | Start Iperf Server | controller | 192.168.1.1 | TC001.log | port=5222 |
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
        Run an iperf3 client on the device and wait for it to finish.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``server_ip`` is the iperf3 server address (``-c``)

        - ``bind_ip`` is the local address to bind to (``-B``)

        - ``protocol`` is ``tcp`` or ``udp``

        - ``log_name`` is the log file on the device (``--logfile``)

        - ``port`` is the server port (``-p``). Defaults to 5201

        - ``time`` is the test duration in seconds (``-t``). The command timeout
          is ``time`` + 1 seconds

        - ``bitrate`` is the target bitrate (``-b``), UDP only

        - ``tos`` is the IP type of service (``-S``)

        - ``window_size`` is the TCP window size (``-w``), TCP only

        - ``mode`` is ``reverse`` (``-R``), ``parallel`` (``-P``) or ``bidir``
          (``--bidir``), or None for a normal test

        - ``parallel_streams`` is the number of parallel streams, required when
          ``mode`` is ``parallel``

        - ``Raises`` ValueError for an invalid protocol, mode or stream count,
          Exception if iperf3 reports an error

        Example:
        | Start Iperf Client | controller_wlan_client_1 | 192.168.1.1 | 192.168.1.20 | tcp | TC001.log | time=10 |
        | Start Iperf Client | controller_wlan_client_1 | 192.168.1.1 | 192.168.1.20 | udp | TC002.log | time=10 | bitrate=100M |
        | Start Iperf Client | controller_wlan_client_1 | 192.168.1.1 | 192.168.1.20 | tcp | TC003.log | time=10 | mode=parallel | parallel_streams=${4} |
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
        Stop all iperf3 processes on the device with ``killall iperf3``.

        - ``device`` is the device name as defined in the infra.yaml config file

        Example:
        | Stop Iperf Server | controller |
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
        Copy an iperf3 log file from the device to the local machine.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``remote_file`` is the log file path on the device

        - ``local_file`` is the local destination path

        Example:
        | Get Iperf Log | controller | /tmp/TC001.log | /home/user/TC001.log |
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
        Copy a file from the local machine to the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``local_file`` is the local file path

        - ``remote_file`` is the destination path on the device

        Example:
        | Put Iperf Log | controller | /home/user/TC001.log | /tmp/TC001.log |
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
        Delete all ``*.log`` files in a directory on the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``dirpath`` is the directory on the device

        - ``Raises`` Exception if the command fails

        Example:
        | Remove Iperf Logs | controller_wlan_client_1 | /tmp |
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
        Delete a log file on the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``filename`` is the file path on the device

        - ``Raises`` Exception if the command fails

        Example:
        | Remove Iperf Log | controller_wlan_client_1 | /tmp/TC001.log |
        """
        zi_logger.log(
            f"lib.map.TrafficGenerator.remove_iperf_log({device})")
        utils_obj = self.get_utils_module_object('traffic_generator')
        utils_obj.remove_iperf_log(device, filename)