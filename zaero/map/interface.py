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
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.platform_modules import PlatformModules
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger

class Interface(DatabaseModule,
                PlatformModules):

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        PlatformModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Interface __init__ : END")

    @keyword("Set Interface From Database")  
    def set_interface_from_database(self,
                                    device: str,
                                    index: str):
        """
        Set the name for an interface,
        which will be derived from the given radio index

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        Example:
        | Set Interface From Database | ap | 2g_radio_index |
        | Set Interface From Database | ap | 5g_radio_index |
        | Set Interface From Database | ap | 6g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_interface_from_database(device,
                                                 index)

    @keyword("Get Interface")
    def get_interface(self,
                      device: str,
                      index: str) -> str:
        """
        Get the name for an interface,
        which will be derived from the given radio index

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the currently configured name of an interface, which has
                      to be validated for an interface

        Example:
        | ${ret} | Get Interface | ap | 2g_radio_index |
        | ${ret} | Get Interface | ap | 5g_radio_index |
        | ${ret} | Get Interface | ap | 6g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        ifname = platform_obj.get_interface(device,
                                            index)
        return ifname

    @keyword("Check Interface")
    def check_interface(self,
                        device: str,
                        index: str):
        """
        Check the name for an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Raise`` exception when the actual wifi-ifname from database is not matched
                    with the configured ifname

        Example:
        | Check Interface | ap | 2g_radio_index |
        | Check Interface | ap | 5g_radio_index |
        | Check Interface | ap | 6g_radio_index |

        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_interface(device,
                                     index)

    @keyword("Set Ssid")
    def set_ssid(self,
                 device: str,
                 index: str,
                 ssid: str,
                 method = 'gui'):
        """
        Set the given Ssid for an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``ssid``  is the name of the wireless network (SSID) to be broadcast
                    which has to be set in the ap for the given interface.

        Example:
        | Set Ssid | ap | 2g_radio_index | 2g_openwrt |
        | Set Ssid | ap | 5g_radio_index | 5g_openwrt |
        | Set Ssid | ap | 6g_radio_index | 6g_openwrt |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_ssid(device, index, ssid, method)

    @keyword("Get Ssid")
    def get_ssid(self,
                 device: str,
                 index: str,
                 method = 'gui') -> str:
        """
        Get the currently configured ssid of an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the currently configured ssid on the
                      device's wireless interface which has
                      to be validated for an interface.

        Example:
        | ${ret} | Get Ssid | ap | 2g_radio_index |
        | ${ret} | Get Ssid | ap | 5g_radio_index |
        | ${ret} | Get Ssid | ap | 6g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        ssid = platform_obj.get_ssid(device, index, method)
        return ssid

    @keyword("Check Ssid")
    def check_ssid(self,
                   device: str,
                   index: str,
                   ssid: str,
                   method = 'gui'):
        """
        Check the currently configured ssid of an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``ssid`` which has to be validated in the ap for the given interface.

        - ``Raise`` exception when the expected ssid is not matched
                    with the configured ssid

        Example:
        | Check Ssid | ap | 2g_radio_index |
        | Check Ssid | ap | 5g_radio_index |
        | Check Ssid | ap | 6g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_ssid(device, index, ssid, method)

    @keyword("Set Encryption")
    def set_encryption(self,
                       device: str,
                       index: str,
                       encryption: str):
        """
        Set the encryption for an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``encryption`` is the encryption method used to secure the wireless network
                         which has to be set in the ap for the given interface

         Example:
        | Set Encryption | ap | 2g_radio_index | psk       |
        | Set Encryption | ap | 5g_radio_index | psk2+ccmp |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_encryption(device,
                                    index,
                                    encryption)

    @keyword("Get Encryption")
    def get_encryption(self,
                       device: str,
                       index: str) -> str:
        """
        Get the currently configured encryption of an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        -  ``Returns`` the currently configured encryption method
                       of an interface which has to be validated

        Example:
        | ${ret} | Get Encryption | ap | 2g_radio_index |
        | ${ret} | Get Encryption | ap | 5g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        encryption = platform_obj.get_encryption(device,
                                                 index)
        return encryption

    @keyword("Set Password")
    def set_password(self,
                     device: str,
                     index: str,
                     password: str):
        """
        Set the password for an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``password`` is the Wi-Fi password used to authenticate clients
                       connecting to the network which has to be set in
                       the ap for the given interface

        Example:
        | Set Password | ap | 2g_radio_index | zilo@123 |
        | Set Password | ap | 5g_radio_index | zilo@123 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_password(device,
                                  index,
                                  password)

    @keyword("Get Password")
    def get_password(self,
                     device: str,
                     index: str) -> str:
        """
        Get the currently configured password of an interface,
        which will be derived from the given radio index.

        - ``device`` is the name refers to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                    as mentioned in the dut.yaml config file

        -  ``Returns`` the currently configured password of an interface which has to be validated

        Example:
        | ${ret} | Get Password | ap | 2g_radio_index |
        | ${ret} | Get Password | ap | 5g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        password =  platform_obj.get_password(device,
                                              index)
        return password

    @keyword("Set Sae Parameters")
    def set_sae_parameters(self,
                           device: str,
                           index: str):
        """
        Set SAE (WPA3) encryption parameters on the specified interface,
        including sae, sae_password, sae_pwe, sae_groups, and en_6g_sec_comp.

        - ``device`` is the name refers to the ap as mentioned
                    in the dut.yaml config file

        - ``index`` is the name refers to the specific radio index
                     as mentioned in the dut.yaml config file

        Example:
        | Set Sae Parameters | ap | 2g_radio_index |
        | Set Sae Parameters | ap | 5g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_sae_parameters(device,
                                        index)

    @keyword("Check Brctl Show")
    def check_brctl_show(self,
                         device: str):
        """
        Executes the 'brctl show' command on the specified device
        to validate the current bridge configuration.

        - ``device`` is the name refers to the ap as mentioned
                    in the dut.yaml config file

        Example:
        | Check Brctl Show | ap |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_brctl_show(device)

    @keyword("Get Dut Bridge Ipv4")
    def get_dut_bridge_ipv4(self,
                            device: str) -> str:
        """
        Get IPV4 address of the bridge interface on the given DUT device.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``Returns`` the IPV4 address of the bridge interface

        Example:
        | ${ret}  |  Get Dut Bridge Ipv4  |  ap  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        ip_address = platform_obj.get_dut_bridge_ipv4(device)
        return ip_address

    @keyword("Get Dut Wan Ipv4")
    def get_dut_wan_ipv4(self,
                     device: str) -> str:
        """
        Get IPV4 address of the WAN interface on the given DUT device.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``Returns`` the IPV4 address of the WAN interface

        Example:
        | ${ret}  |  Get Dut Wan Ipv4  |  ap  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        ip_address = platform_obj.get_dut_wan_ipv4(device)
        return ip_address

    @keyword("Set Wifi Iface Device")
    def set_wifi_iface_device(self,
                          device: str,
                          index: str,
                          if_device: str):
        """
        Set the wifi-iface device (e.g., wifi0, wifi1) for the given radio index.

        - ``device`` refers to the AP name from dut.yaml
        - ``index`` refers to the radio index (2g_radio_index, 5g_radio_index, etc.)
        - ``if_device`` is the wifi device to map (e.g., wifi0, wifi1)

        Example:
        | Set Wifi Iface Device | ap | 2g_radio_index | wifi0 |
        | Set Wifi Iface Device | ap | 5g_radio_index | wifi1 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        wifi_iface = platform_obj.set_wifi_iface_device(device, index, if_device)
        return wifi_iface


    @keyword("Get Wifi Iface Device")
    def get_wifi_iface_device(self,
                            device: str,
                            index: str,
                            expected_if_device: str = None):
        """
        Return the wifi-iface device (wifi0, wifi1, etc.) for the given radio index.
        If expected_if_device is provided, validate it; otherwise just return the value.
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        wifi_iface = platform_obj.get_wifi_iface_device(device, index, expected_if_device)
        return wifi_iface

    @keyword("Set Wifi Iface Network")
    def set_wifi_iface_network(self,
                               device: str,
                               index:str,
                                if_network: str):
        """
        Set the network for the specified wifi interface
        (e.g., uci set wireless.@wifi-iface[1].network='lan').

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``if_network`` is the network name to assign (e.g., lan, wan)

        Example:
        | Set Wifi Iface Network | ap | 2g_radio_index | lan |
        | Set Wifi Iface Network | ap | 5g_radio_index | lan |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        wifi_network = platform_obj.set_wifi_iface_network(device, index, if_network)
        return wifi_network

    @keyword("Get Wifi Iface Network")
    def get_wifi_iface_network_keyword(self, device: str, index: str):
        """
        Robot Framework keyword to get the network assigned to a wifi interface.

        - device: Device name from the database
        - index: Radio index key (e.g., 2g_radio_index, 5g_radio_index)

        Returns:
        - Network name assigned to the interface.
        """
        zi_logger.print_context()

        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)

        return platform_obj.get_wifi_iface_network(device, index)



    @keyword("Set Wifi Iface Mode")
    def set_wifi_iface_mode(self,
                            device: str,
                            index: str,
                            if_mode: str):
        """
        Set the operating mode for the specified wifi interface
        (e.g., uci set wireless.@wifi-iface[1].mode='ap').

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``if_mode`` is the mode to set (e.g., ap, sta, monitor)

        Example:
        | Set Wifi Iface Mode | ap | 2g_radio_index | ap  |
        | Set Wifi Iface Mode | ap | 5g_radio_index | sta |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        wifi_mode = platform_obj.set_wifi_iface_mode(device, index, if_mode)
        return  wifi_mode

    @keyword("Get Wifi Iface Mode")
    def get_wifi_iface_mode_keyword(self, device: str, index: str):
        """
        Robot Framework keyword to get the mode assigned to a wifi interface.

        - device: Device name from the database
        - index: Radio index key (e.g., 2g_radio_index, 5g_radio_index)

        Returns:
        - Mode of the interface (e.g., ap, sta).
        """
        zi_logger.print_context()

        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_wifi_iface_mode(device, index)

    @keyword("Check Mode")
    def check_mode(self,
                   device: str,
                   index: str,
                   mode: str):
        """
        Verify that the wifi interface is operating in the expected mode
        by reading the live mode from the device via iw.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``mode`` is the expected mode (e.g., AP, managed, monitor)

        - ``Raises`` RuntimeError if the actual mode does not match

        Example:
        | Check Mode | ap | 2g_radio_index | AP |
        | Check Mode | ap | 5g_radio_index | AP |
        """
        zi_logger.print_context()

        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.check_mode(device, index , mode)


    @keyword("Set Isolate")
    def set_wifi_iface_isolate(self,
                                device: str,
                                index: str,
                                isolate: int):
        """
        Enable or disable client isolation on the specified wifi interface.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``isolate`` is 1 to enable client isolation, 0 to disable

        Example:
        | Set Isolate | ap | 2g_radio_index | 1 |
        | Set Isolate | ap | 5g_radio_index | 0 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        wifi_isolate = platform_obj.set_wifi_iface_isolate(device, index, isolate)
        return  wifi_isolate

    @keyword("Get Isolate")
    def get_wifi_iface_isolate(self,
                                device: str,
                                index: str):
        """
        Retrieve the client isolation setting of the specified wifi interface.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``Returns`` '1' if client isolation is enabled, '0' if disabled

        Example:
        | ${ret} | Get Isolate | ap | 2g_radio_index |
        | ${ret} | Get Isolate | ap | 5g_radio_index |
        """
        zi_logger.print_context()

        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_wifi_iface_isolate(device, index)


    @keyword("Add Wifi Interface")
    def add_wifi_interface(self,
                            device : str):
        """
        Add a new wifi-iface section on the device and update the local
        interface index list in the database.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        Example:
        | Add Wifi Interface | ap |
        """
        zi_logger.print_context()

        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.add_wifi_interface(device)

    @keyword("Delete Wifi Interface")
    def delete_wifi_interface(self,
                          device: str,
                          vap_name: str):
        """
        Delete a wifi-iface section identified by its VAP name from the device.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``vap_name`` is the name assigned to the VAP (used to locate the interface)

        Example:
        | Delete Wifi Interface | ap | vap0 |
        | Delete Wifi Interface | ap | vap1 |
        """
        zi_logger.print_context()

        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.delete_wifi_interface(device, vap_name)

    @keyword("Set Vap Device")
    def set_vap_device(self,
                        device: str,
                        index: str,
                        radio: str):
        """
        Set the radio device (e.g., wifi0, wifi1) for the specified wifi interface.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``radio`` is the radio device name to assign (e.g., wifi0, wifi1)

        Example:
        | Set Vap Device | ap | 2g_radio_index | wifi0 |
        | Set Vap Device | ap | 5g_radio_index | wifi1 |
        """
        zi_logger.print_context()

        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.set_vap_device(device, index , radio)

    @keyword("Get Vap Device")
    def get_vap_device(self,
                        device: str,
                        index: str):
        """
        Retrieve the radio device (e.g., wifi0, wifi1) assigned to the
        specified wifi interface.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``Returns`` the radio device name assigned to the wifi interface

        Example:
        | ${ret} | Get Vap Device | ap | 2g_radio_index |
        | ${ret} | Get Vap Device | ap | 5g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_vap_device(device, index )

    @keyword("Set Vap Name")
    def set_vap_name(self,
                        device: str,
                        index: str,
                        name: str):
        """
        Set the name identifier for the specified wifi interface.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``name`` is the VAP name to assign to the interface

        Example:
        | Set Vap Name | ap | 2g_radio_index | vap0 |
        | Set Vap Name | ap | 5g_radio_index | vap1 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.set_vap_name(device, index, name )


    @keyword("Get Vap name")
    def get_vap_name(self,
                        device: str,
                        index: str):
        """
        Retrieve the name identifier of the specified wifi interface.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``Returns`` the VAP name assigned to the interface

        Example:
        | ${ret} | Get Vap Name | ap | 2g_radio_index |
        | ${ret} | Get Vap Name | ap | 5g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.get_vap_name(device, index )

    @keyword("check Vap Mode")
    def check_vap_mode(self,
                        device: str,
                        vap_index:str,
                        mode: str):
        """
        Verify that the VAP identified by its SSID is operating in the expected mode.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``vap_index`` is the SSID of the VAP to look up

        - ``mode`` is the expected mode (e.g., AP, managed)

        - ``Returns`` True if the mode matches, False otherwise

        Example:
        | ${ret} | Check Vap Mode | ap | Openwrt | AP |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.check_vap_mode(device, vap_index , mode)

    @keyword("Check Vap Ssid")
    def check_vap_ssid(self,
                        device: str,
                        vap_index: str,
                        vap_ssid:str):
        """
        Verify that the VAP identified by its SSID is broadcasting the expected SSID.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``vap_index`` is the SSID used to locate the VAP interface

        - ``vap_ssid`` is the expected SSID to verify

        - ``Returns`` the actual SSID read from the interface

        Example:
        | ${ret} | Check Vap Ssid | ap | Openwrt | Openwrt |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.check_vap_ssid(device, vap_index , vap_ssid)

    @keyword("Set Interface State")
    def set_interface_state(self,
                        device: str,
                        index: str,
                        state: int):
        """
        Enable or disable the specified wifi interface via UCI.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``state`` is the desired state: True to enable, False to disable

        Example:
        | Set Interface State | ap | 2g_radio_index | True  |
        | Set Interface State | ap | 5g_radio_index | False |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_interface_state(device,
                                     index,
                                     state)
    @keyword("Get Interface State")
    def get_interface_state(self,
                        device: str,
                        index: str) -> bool:
        """
        Retrieve the enabled/disabled state of the specified wifi interface.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``Returns`` 1 if the interface is enabled, 0 if disabled

        Example:
        | ${ret} | Get Interface State | ap | 2g_radio_index |
        | ${ret} | Get Interface State | ap | 5g_radio_index |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        state = platform_obj.get_interface_state(device,
                                                 index)
        return state

    def reboot_device(self,
                      device: str,
                      method = 'gui'):
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.reboot_device(device,
                                   method)
        
    def wifi_reset(self,
                   device: str,
                   method = 'gui'):
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.wifi_reset(device,
                                method)
