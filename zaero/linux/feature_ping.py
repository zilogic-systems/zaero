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
Linux implementation of the ping methods.

Author: Zilogic Systems <code@zilogic.com>
"""
# Standard Libraries
import re

# Local Libraries
from zaero.base.base_feature_ping import BaseFeaturePing
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger


class FeaturePing(BaseFeaturePing,
                  DatabaseModule,
                  ConnectionModules):
    """
    Ping methods for Linux hosts. Pings are sent from the ``data_iface`` of the device.
    """
    
    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log("Linux.FeaturePing __init__ : END")
    
    def ping_ipv4(self,
                  device: str,
                  dst_ip: str,
                  count: int) -> int:
        """
        Ping an IPv4 destination with ``ping -4 -I <data_iface> -c <count>``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``dst_ip`` is the destination address or host name

        - ``count`` is the number of packets to send

        - ``Returns`` the packet loss in percent as an integer

        - ``Raises`` Exception if the command fails or the packet loss is not
          found in the output
        """
        zi_logger.print_context()
        interface = self.db_obj.read_from_database(device, 'data_iface')
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        command = f"ping -4 -I {interface} -c {count} {dst_ip}"
        output, error = connection_obj.execute_command(device, command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        zi_logger.log(f"Ping ipv4 output:\n {output}")

        match = re.search(r'(\d+)% packet loss', output)
        if match:
            packet_loss = int(match.group(1))
            return packet_loss
        else:
            raise Exception("Packet loss value not found in output")

    def ping_ipv6(self,
                  device: str,
                  dst_ip: str,
                  count: int) -> int:
        """
        Ping an IPv6 destination with ``ping -6 -I <data_iface> -c <count>``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``dst_ip`` is the destination address or host name

        - ``count`` is the number of packets to send

        - ``Returns`` the packet loss in percent as an integer

        - ``Raises`` Exception if the command fails or the packet loss is not
          found in the output
        """
        zi_logger.print_context()
        interface = self.db_obj.read_from_database(device, 'data_iface')
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        command = f"ping -6 -I {interface} -c {count} {dst_ip}"
        output, error = connection_obj.execute_command(device, command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        zi_logger.log(f"Ping ipv6 output:\n {output}")

        match = re.search(r'(\d+)% packet loss', output)
        if match:
            packet_loss = int(match.group(1))
            return packet_loss
        else:
            raise Exception("Packet loss value not found in output")
