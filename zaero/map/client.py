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
Robot Framework keywords for WiFi and LAN client operations.

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
    Keywords for client devices (Linux, Android). Each keyword reads the
    ``platform`` of the device and calls the same method on that platform
    plugin.
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
        Get the operating system name of the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the OS name, e.g. ``Linux`` (output of ``uname``)

        Example:
        | ${ret} | Get Client Os | controller_wlan_client_1 |
        | ${ret} | Get Client Os | extender1_wlan_client_1  |
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
        Get the IPv4 address of the ``data_iface`` of the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the IPv4 address as a string

        Example:
        | ${ret} | Get Client Ipv4 | controller_wlan_client_1 |
        | ${ret} | Get Client Ipv4 | extender1_wlan_client_1  |
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
        Turn the WiFi radio of the client device on or off.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``state`` is ``1`` to turn the radio on, ``0`` to turn it off

        - ``Raises`` Exception if the command fails

        Example:
        | Set Client Radio State | controller_wlan_client_1 | 0 |
        | Set Client Radio State | controller_wlan_client_1 | 1 |
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
        Get the WiFi radio state of the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` ``1`` if the radio is enabled, ``0`` if it is disabled

        Example:
        | ${ret} | Get Client Radio State | controller_wlan_client_1 |
        | ${ret} | Get Client Radio State | extender1_wlan_client_1  |
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
        Bring the ``data_iface`` of the client device up or down.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``state`` is ``1`` to bring the interface up, ``0`` to bring it down

        - ``Raises`` ValueError if the interface is missing or is not a WiFi or
          Ethernet interface, Exception if the command fails

        Example:
        | Set Client Interface State | controller_lan_client_1  | 0 |
        | Set Client Interface State | controller_wlan_client_1 | 1 |
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
        Get the state of the ``data_iface`` of the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` ``1`` if the interface is up, ``0`` if it is down

        Example:
        | ${ret} | Get Client Interface State | controller_wlan_client_1 |
        | ${ret} | Get Client Interface State | extender1_wlan_client_1  |
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
        Check that the given SSID is visible in the WiFi scan of the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to look for

        - ``Raises`` Exception if the radio is off or the SSID is not visible

        Example:
        | Check Ap Ssid Visibility | controller_wlan_client_1 | OpenWrt |
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
        Get the BSSID of the access point broadcasting the given SSID, as seen in
        the WiFi scan of the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to look for

        - ``Returns`` the BSSID (MAC address) of the first matching scan entry,
          or None if it is not found

        - ``Raises`` Exception if the radio is off or the scan fails

        Example:
        | ${bssid} | Get Ap Bssid Visibility | controller_wlan_client_1 | OpenWrt |
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
                               bssid: str = None,
                               hidden:str = False):
        """
        Connect the client device to a WiFi network.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to connect to

        - ``password`` is the network password. Give it for secured networks,
          leave it as None for open networks

        - ``bssid`` if given, connect to and lock the connection to the access
          point with this BSSID (Linux clients only)

        - ``hidden`` set to True if the SSID is hidden. Defaults to False

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface,
          Exception or RuntimeError if a command fails

        Example:
        | Connect Client To Ssid | controller_wlan_client_1 | OpenWrt |
        | Connect Client To Ssid | controller_wlan_client_1 | OpenWrt | 12345678 |
        | Connect Client To Ssid | controller_wlan_client_1 | OpenWrt | 12345678 | hidden=True |
        | Connect Client To Ssid | extender1_wlan_client_1  | OpenWrt | 12345678 | bssid=aa:bb:cc:dd:ee:ff |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.connect_client_to_ssid(device,
                                            ssid,
                                            password,
                                            bssid,
                                            hidden)

    @keyword("Get Client Connected Ssid")
    def get_client_connected_ssid(self,
                                  device: str) -> str:
        """
        Get the SSID the client device is currently connected to.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the SSID as a string

        Example:
        | ${ret} | Get Client Connected Ssid | controller_wlan_client_1 |
        | ${ret} | Get Client Connected Ssid | extender1_wlan_client_1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_connected_ssid(device)
    
    @keyword("Get Client Channel")
    def get_client_channel(self,
                           device: str) -> int:
        """
        Get the channel of the WiFi network the client device is connected to.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the channel number as an integer

        Example:
        | ${ret} | Get Client Channel | controller_wlan_client_1 |
        | ${ret} | Get Client Channel | extender1_wlan_client_1  |
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
        Delete a saved network connection on the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``connection_name`` is the name of the connection. For a WiFi
          connection it is normally the SSID. Android clients ignore it and
          forget the currently connected network

        - ``Raises`` TypeError if the ``data_iface`` is not a WiFi or Ethernet
          interface, RuntimeError if the connection could not be deleted

        Example:
        | Remove Client Connection | controller_wlan_client_1 | OpenWrt |
        """
        zi_logger.log(f"map.client.remove_client_connection({device}, {connection_name})")
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.remove_client_connection(device,connection_name)
    
    @keyword("Remove All Wifi Connections")
    def remove_all_wifi_connections(self,
                                    device: str):
        """
        Delete all saved WiFi connections on the client device.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Raises`` TypeError if the ``data_iface`` is not a WiFi interface,
          RuntimeError if a connection could not be deleted

        Example:
        | Remove All Wifi Connections | controller_wlan_client_1 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.remove_all_wifi_connections(device)

    @keyword("Get Client Bandwidth")
    def get_client_bandwidth(self,
                             device: str) -> str:
        """
        Get the channel width of the WiFi network the client device is connected to.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the channel width as a string, e.g. ``80 MHz``

        Example:
        | ${ret} | Get Client Bandwidth | controller_wlan_client_1 |
        | ${ret} | Get Client Bandwidth | extender1_wlan_client_1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_bandwidth(device)

    @keyword("Get Client Encryption")
    def get_client_encryption(self,
                              device: str) -> str:
        """
        Get the key management of the WiFi network the client device is connected to.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the ``key_mgmt`` value from ``wpa_cli status``, e.g. ``WPA2-PSK``

        Example:
        | ${ret} | Get Client Encryption | controller_wlan_client_1 |
        | ${ret} | Get Client Encryption | extender1_wlan_client_1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_encryption(device)
    
    @keyword("Get Client Frequency")
    def get_client_frequency(self,
                             device: str) -> int:
        """
        Get the frequency of the WiFi network the client device is connected to.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the frequency in MHz

        Example:
        | ${ret} | Get Client Frequency | controller_wlan_client_1 |
        | ${ret} | Get Client Frequency | extender1_wlan_client_1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_frequency(device)

    @keyword("Get Client Rssi")
    def get_client_rssi(self,
                        device: str) -> str:
        """
        Get the signal strength of the WiFi network the client device is connected to.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Returns`` the signal strength as a string, e.g. ``-45dBm``

        Example:
        | ${ret} | Get Client Rssi | controller_wlan_client_1 |
        | ${ret} | Get Client Rssi | extender1_wlan_client_1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_client_rssi(device)

    @keyword("Disconnect Wifi Client")
    def disconnect_wifi_client(self,
                               device: str):
        """
        Disconnect the client device from its current WiFi network.

        - ``device`` is the client name as defined in the infra.yaml config file

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or
          the device could not be disconnected

        Example:
        | Disconnect Wifi Client | controller_wlan_client_1 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.disconnect_wifi_client(device) 

