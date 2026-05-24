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
This library provides keywords to handle basic network reachability functions
for various clients across different platforms, including Windows and Linux.

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
    This library provides keywords to handle basic network reachability functions
    for various clients across different platforms, including Windows and Linux.
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
        Ping from specified device to destination ipv4 address.

        - ``device`` The name of the client or DUT as defined in the config file.

        - ``dst_ip`` The destination IPv4 address to be pinged.
        
        - ``count`` The number of ICMPv4 packets to send.
        
        - ``Returns`` Packet loss as a percentage string. Example: 0.

        Example:
        | ${ret} | Ping Ipv4 |        ap        | google.com  | 4 |
        | ${ret} | Ping Ipv4 | ap_lan_client_1  | 192.168.1.1 | 4 |
        | ${ret} | Ping Ipv4 | ap_wlan_client_1 | 192.168.1.1 | 4 |

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
        Ping from specified device to destination ipv6 address.

        - ``device`` The name of the client or DUT as defined in the config file.

        - ``dst_ip`` The destination IPv6 address to be pinged.
        
        - ``count`` The number of ICMPv6 packets to send.
        
        - ``Returns`` Packet loss as a percentage string. Example: 0.

        Example:
        | ${ret} | Ping Ipv6 |        ap        |       google.com     | 4 |
        | ${ret} | Ping Ipv6 | ap_lan_client_1  | 2001:4860:4860::8888 | 4 |
        | ${ret} | Ping Ipv6 | ap_wlan_client_1 | 2001:4860:4860::8888 | 4 |

        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        loss = platform_obj.ping_ipv6(device, dst_ip, count)
        return loss
