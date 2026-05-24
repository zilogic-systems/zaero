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
This module handles various client operation

Author: Zilogic Systems <code@zilogic.com>
"""
# Third-party Libraries
from robot.api.deco import keyword

# Local Libraries
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.platform_modules import PlatformModules
import zaero.utils.zi_logger as zi_logger

class Client(DatabaseModule,
             PlatformModules):
    """
    This library provides keywords to handles basic functionality 
    for various client across different platforms including Windows, 
    Linux, Android, and iOS.
    """
    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        PlatformModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Client __init__ : END")
    
    @keyword("Get Client Os")
    def get_client_os(self,
                      device: str) -> str:
        """
        Get OS name of the specified device.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``Returns`` the OS name of the given client device

        Example:
        | ${ret} = | Get Client Os | ap_lan_client_1  |
        | ${ret} = | Get Client Os | ap_wlan_client_1 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        operating_system = platform_obj.get_client_os(device)
        return operating_system

    
    @keyword("Get Client Ipv4")
    def get_client_ipv4(self,
                        device: str) -> str:
        """
        Get IPV4 address of the given client device.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``Returns`` the IPV4 address of the given client device

        Example:
        | ${ret}  |  Get Client Ipv4  |  ap_lan_client_1   |
        | ${ret}  |  Get Client Ipv4  |  ap_wlan_client_1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        ip_address = platform_obj.get_client_ipv4(device)
        return ip_address

    
    @keyword("Set Client Radio State")
    def set_client_radio_state(self,
                               device:str,
                               state: int):
        """
        Enable or disable radio of the given wlan client device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``state`` is the desired state of the radio

            ``state == 1``, Turns the radio ON
            
            ``state == 0``, Turns the radio OFF

        Example:
        | Set Client Radio State  |  ap_wlan_client_1  |  0  |
        | Set Client Radio State  |  ap_wlan_client_1  |  1  |
        | Set Client Radio State  |  ap_wlan_client_2  |  0  |
        | Set Client Radio State  |  ap_wlan_client_2  |  1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_client_radio_state(device,
                                            state)

    @keyword("Get Client Radio State")
    def get_client_radio_state(self,
                               device:str) -> int:
        """
        Retrieve the radio state given wlan client device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` specify the radio state whether it's enabled/disabled.

            ``Enabled - 1``

            ``Disabled - 0``

        Example:
        | ${ret} | Get Client Radio State  |  ap_wlan_client_1  |
        | ${ret} | Get Client Radio State  |  ap_wlan_client_2  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        output = platform_obj.get_client_radio_state(device)
        return output
        
    
    @keyword("Set Client Interface State")
    def set_client_interface_state(self,
                                   device:str,
                                   state: int):
        """
        Enable or disable interface of the given client device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``state`` is the desired state of the radio
        
        ``state == 1``, Interface ON

        ``state == 0``, Interface OFF

        Example:
        | Set Client Interface State  |  ap_lan_client_1   |  0  |
        | Set Client Interface State  |  ap_lan_client_1   |  1  |
        | Set Client Interface State  |  ap_wlan_client_1  |  0  |
        | Set Client Interface State  |  ap_wlan_client_1  |  1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_client_interface_state(device,
                                                state)

    @keyword("Get Client Interface State")
    def get_client_interface_state(self,
                                   device:str) -> int:
        """
        Retrieve the interface state whether it's enabled/disabled for 
        given client device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` specify the interface state whether it's enabled/disabled.
        
            ``Enabled - 1`` (Interface up)

            ``Disabled - 0`` (Interface down)

        Example:
        | ${ret} | Get Client Interface State  |  ap_lan_client_1  |
        | ${ret} | Get Client Interface State  |  ap_wlan_client_1 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        output = platform_obj.get_client_interface_state(device)
        return output
        
    
    @keyword("Check Ap Ssid Visibility")
    def check_ap_ssid_visibility(self,
                                 device: str,
                                 ssid: str):
        """
        Verifies if the ssid configured on the AP is visible to the client device.

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``ssid`` Specified a given ssid name.

        - ``Raise`` exception when the scanned ssid doesn't match
                    the expected ssid.
        Example:
        | Check Ap Ssid Visibility | ap_wlan_client_1 | Openwrt |
        | Check Ap Ssid Visibility | ap_wlan_client_2 | Openwrt |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_ap_ssid_visibility(device,ssid)
            
    @keyword("Get Ap Bssid Visibility")
    def get_client_bssid_visibility(self,
                                    device: str,
                                    ssid: str) -> str:
        """
        Retrieve the BSSID for the given SSID.

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``ssid`` Specified a given ssid name.

        - ``Returns`` specifies the availability of bssid name.

        Example:
        | ${ret} | Get Ap Bssid Visibility | ap_wlan_client_1 | Openwrt |
        | ${ret} | Get Ap Bssid Visibility | ap_wlan_client_2 | Openwrt |

        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        output = platform_obj.get_ap_bssid_visibility(device,
                                                      ssid)
        return output

    @keyword("Connect Client To Ssid")
    def connect_client_to_ssid(self,
                               device: str,
                               ssid: str,
                               password: str = None,
                               hidden:str = False):
        """
        Connect a client device to the specified WiFi SSID.

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``ssid`` Specified a given ssid name.

        - ``password`` to connect with the WiFi network,
                     It has to be provided to connect with secured networks.
                     And should not be provided for open networks.

        - ``hidden`` Set to True if the SSID is hidden. Defaults to False.

        - ``Raise`` exception when the device interface is wrong
                     or ssid can't be found.

        Example:
        | Connect Client To Ssid | ap_wlan_client_1 | Openwrt |
        | Connect Client To Ssid | ap_wlan_client_1 | Openwrt | 12345678 |
        | Connect Client To Ssid | ap_wlan_client_1 | Openwrt | hidden=True |
        | Connect Client To Ssid | ap_wlan_client_1 | Openwrt | 12345678 | hidden=True |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.connect_client_to_ssid(device,
                                            ssid,
                                            password,
                                            hidden)

    @keyword("Get Client Connected Ssid")
    def get_client_connected_ssid(self,
                                  device: str) -> str:
        """
        Retrieve the SSID to which the client device connected currently.

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` The SSID of the connected WiFi network.

        Example:
        | ${ret} = | Get Client Connected Ssid | ap_wlan_client_1 |
        | ${ret} = | Get Client Connected Ssid | ap_wlan_client_2 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_connected_ssid(device)
    
    @keyword("Get Client Channel")
    def get_client_channel(self,
                           device: str) -> int:
        """
        Retrieve the channel of the currently connected WiFi network on the
        specified device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` The channel used by the currently connected Wi-Fi network.

        Example:
        | ${ret} | Get Client Channel | ap_wlan_client_1 |
        | ${ret} | Get Client Channel | ap_wlan_client_2 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_channel(device)
 
    @keyword("Remove Client Connection")
    def remove_client_connection(self,
                                 device: str,
                                 connection_name: str):
        """
        Remove the connection based on name assigned to the connection.

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file
                     
        - ``connection_name`` is the name assigned to the specific connection.

                              Ex: For wifi interface, We should consider ssid as connection name.

        Example:
        | Remove Client Connection | ap_wlan_client_1 | OpenWrt |
        """
        zi_logger.log(f"map.client.remove_client_connection({device}, {connection_name})")
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.remove_client_connection(device,connection_name)
    
    @keyword("Remove All Wifi Connections")
    def remove_all_wifi_connections(self,
                                    device: str):
        """
        Remove all wifi connections based on device.

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        Example:
        | Remove All Wifi Connections | ap_wlan_client_1 |
        | Remove All Wifi Connections | ap_wlan_client_2 |

        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.remove_all_wifi_connections(device)

    @keyword("Get Client Bandwidth")
    def get_client_bandwidth(self,
                             device: str) -> str:
        """
        Retrieve the bandwidth of the currently connected WiFi network on the
        specified device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` The bandwidth used by the currently connected Wi-Fi network.

        Example:
        | ${ret} | Get Client Bandwidth | ap_wlan_client_1 |
        | ${ret} | Get Client Bandwidth | ap_wlan_client_2 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_bandwidth(device)

    @keyword("Get Client Encryption")
    def get_client_encryption(self,
                              device: str) -> str:
        """
        Retrieve the encryption of the currently connected WiFi network on the
        specified device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` The encryption type used by the currently connected Wi-Fi network.

        Example:
        | ${ret} | Get Client Encryption | ap_wlan_client_1 |
        | ${ret} | Get Client Encryption | ap_wlan_client_2 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_encryption(device)
    
    @keyword("Get Client Frequency")
    def get_client_frequency(self,
                             device: str) -> int:
        """
        Retrieve the frequency of the currently connected WiFi network on the
        specified device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` The frequency used by the currently connected Wi-Fi network.

        Example:
        | ${ret} | Get Client Frequency | ap_wlan_client_1 |
        | ${ret} | Get Client Frequency | ap_wlan_client_2 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_frequency(device)

    @keyword("Get Client Rssi")
    def get_client_rssi(self,
                        device: str) -> str:
        """
        Retrieve the RSSI value of the currently connected WiFi network on the
        specified device

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        - ``Returns`` The RSSI value used by the currently connected Wi-Fi network.

        Example:
        | ${ret} | Get Client Rssi | ap_wlan_client_1 |
        | ${ret} | Get Client Rssi | ap_wlan_client_2 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_rssi(device)

    @keyword("Disconnect Wifi Client")
    def disconnect_wifi_client(self,
                               device: str):
        """
        Disconnect the wifi client from the currently connected wireless network.

        - ``device`` is the name given to the client as mentioned
                     in the dut.yaml config file

        Examples:
        | Disconnect Wifi Client | ap_wlan_client_1 |
        | Disconnect Wifi Client | ap_wlan_client_2 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.disconnect_wifi_client(device) 

