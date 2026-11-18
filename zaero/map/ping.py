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
Robot Framework keywords to check network reachability.

Author: Zilogic Systems <code@zilogic.com>
"""
# Third-party Libraries
from robot.api.deco import keyword

# Local Libraries
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.platform_modules import PlatformModules
import zaero.utils.zi_logger as zi_logger


class Ping(DatabaseModule,
           PlatformModules):
    """
    Ping keywords. Each keyword reads the ``platform`` of the device and
    calls the ping method of that platform plugin.
    """
    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        PlatformModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Ping __init__ : END")
    
    @keyword("Ping Ipv4")
    def ping_ipv4(self,
                  device: str,
                  dst_ip: str,
                  count: int) -> str:
        """
        Ping an IPv4 destination from the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``dst_ip`` is the IPv4 address or host name to ping

        - ``count`` is the number of ICMP packets to send

        - ``Returns`` the packet loss in percent as an integer, e.g. ``0``

        - ``Raises`` Exception if the ping fails or the packet loss is not
          found in the output

        Example:
        | ${loss} | Ping Ipv4 | controller_lan_client_1  | 192.168.1.1 | 4 |
        | ${loss} | Ping Ipv4 | controller_wlan_client_1 | 8.8.8.8     | 4 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        loss = platform_obj.ping_ipv4(device, dst_ip, count)
        return loss

    @keyword("Ping Ipv6")
    def ping_ipv6(self,
                  device: str,
                  dst_ip: str,
                  count: int) -> str:
        """
        Ping an IPv6 destination from the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``dst_ip`` is the IPv6 address or host name to ping

        - ``count`` is the number of ICMPv6 packets to send

        - ``Returns`` the packet loss in percent as an integer, e.g. ``0``

        - ``Raises`` Exception if the ping fails or the packet loss is not
          found in the output

        Example:
        | ${loss} | Ping Ipv6 | controller_wlan_client_1 | fe80::1 | 4 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        loss = platform_obj.ping_ipv6(device, dst_ip, count)
        return loss
