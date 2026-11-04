# Copyright 2024 Zilogic Systems
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

import string
import random

import paramiko

from scp import SCPClient
from robot.api.deco import keyword

from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger
import logging
import time


logging.getLogger("paramiko").setLevel(logging.CRITICAL)

class TrafficGenerator(DatabaseModule, ConnectionModules):
    """
    This module provides generic functionalities for generating network traffic using SSH,
    including support for TCP, UDP, and multicast traffic flows.
    """
    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log("generic.TrafficGenerator.__init__ : END")
    
    def start_iperf_server(self, # pylint: disable=R0913
                           device: str,
                           bind_ip: str,
                           log_name: str,
                           port: int = 5201):
        """
        Generate an iperf server and store logs locally.
        """
        zi_logger.log(
            f"generic.generic_traffic_generator.start_iperf_server({device},"
            f"{bind_ip}, {log_name}, {port})"
            )
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        
        log_file = f"{log_name}"

        cmd_parts = [
            "iperf3 -s",
            f"-B {bind_ip}",
            f"-p {port}",
            f"--logfile {log_name}"
        ]
        filter_cmd_parts = list(filter(None, cmd_parts))
        command = " ".join(filter_cmd_parts)

        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True,
                                               blocking_call=False)
        if error:
            raise Exception(f"Failed to start iPerf server: {error}")

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
        Generate an iperf client and store logs locally.
        """
        zi_logger.log(
            f"generic.generic_traffic_generator.start_iperf_client({device},"
            f"{server_ip}, {bind_ip}, {protocol}, {log_name}, {port}, {time},"
            f"{bitrate}, {tos}, {window_size}, {mode}, {parallel_streams})"
        )

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        

        protocol = protocol.lower()
        if protocol not in ('tcp', 'udp'):
            raise ValueError(f"Invalid protocol '{protocol}'. Must be 'tcp' or 'udp'")

        modes = [None, 'parallel', 'bidir', 'reverse']
        if mode and mode.lower() not in modes:
            raise ValueError(f"Mode '{mode}' not supported. Choose from {modes}")

        cmd_parts = [
            f"iperf3 -c {server_ip}",
            f"-B {bind_ip}",
            f"-p {port}",
            f"-t {time}",
            f"--logfile {log_name}",
            "-u" if protocol == "udp" else ""
        ]

        if mode:
            mode = mode.lower()
            if mode == "reverse":
                cmd_parts.append("-R")
            elif mode == "parallel":
                if not isinstance(parallel_streams, int) or parallel_streams < 1:
                    raise ValueError("Parallel mode requires a valid stream count (parallel_streams ≥ 1).")
                cmd_parts.append(f"-P {parallel_streams}")
            elif mode == "bidir":
                cmd_parts.append("--bidir")

        if tos:
            cmd_parts.append(f"-S {tos}")

        if bitrate and protocol == "udp":
            cmd_parts.append(f"-b {bitrate}")

        if window_size and protocol == "tcp":
            cmd_parts.append(f"-w {window_size}")

        filter_cmd_parts = list(filter(None, cmd_parts))
        command = " ".join(filter_cmd_parts)

        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True,
                                               timeout= time + 1 if time else None)
        if error:
            raise Exception(f"Failed to run iPerf client: {error}")
        
    def stop_iperf_server(self,
                          device: str):
        """
        Stop the iperf server using pkill command
        """
        zi_logger.log(
            f"generic.feature_traffic_generator.stop_iperf_server({device})"
            )
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        platform = self.db_obj.read_from_database(device, 'platform')

        command = "killall iperf3"

        connection_obj.execute_command(device, command,
                                       return_stdout=False,
                                       return_stderr=True)

    def remove_iperf_logs(self,
                          device: str,
                          dirpath: str):
        """
        Remove Iperf Logs From specified device and specified directory.
        """
        zi_logger.log(
            f"generic.feature_traffic_generator.remove_iperf_logs({device}, {dirpath})"
            )
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        
        command = f"rm {dirpath}/*.log"

        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")

    def remove_iperf_log(self,
                         device: str,
                         filename: str):
        """
        Remove Iperf Log From specified device.
        """
        zi_logger.log(
            f"generic.feature_traffic_generator.remove_iperf_log({device}, {filename})"
            )
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        
        
        command = f"rm {filename}"

        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True)

        if error:
            raise Exception(f"Command execution failed : {command}")

    def get_iperf_log(self,
                      device: str,
                      remote_file: str,
                      local_file: str):
        """
        Retrieve a iperf log from the remote machine.
        """
        zi_logger.log(
            f"generic.generic_traffic_generator.get_iperf_log({device},"
            f"{remote_file}, {local_file}")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        
        connection_obj.get_file(remote_file, local_file)

    def put_iperf_log(self,
                      device: str,
                      local_file: str,
                      remote_file: str):
        """
        Transfer a file from the local machine to the remote machine.
        """
        zi_logger.log(
            f"generic.generic_traffic_generator.put_iperf_log({device},"
            f"{local_file}, {remote_file}")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        
        connection_obj.put_file(local_file, remote_file)
