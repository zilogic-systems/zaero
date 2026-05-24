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
This module handles Android WiFi client operations
such as connecting, disconnecting, and status checking.

Author: Zilogic Systems <code@zilogic.com>
"""
# Standard Libraries
import time
import ast
import re

# Local Libraries
from zaero.base.base_feature_client import BaseFeatureClient
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger



class FeatureClient(BaseFeatureClient,
                    DatabaseModule,
                    ConnectionModules):
    """Handles basic WiFi functionality keywords for Android client."""

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log("android.feature_client.FeatureClient.__init__ : END")

    def __get_device_id(self, device: str) -> str:
        zi_logger.print_context()
        device_id = self.db_obj.read_from_database(device, 'device_id')
        zi_logger.log(f"device_id={device_id}")
        if not device_id:
            raise ValueError(f"Device id  not found in this {device} device.")
        return device_id

    def __get_interface(self,
                        device: str) -> str:
        """
        Get data interface from the specified device.
        """
        zi_logger.print_context()
        interface = self.db_obj.read_from_database(device, 'data_iface')
        zi_logger.log(f"interface={interface}")
        if not interface:
            raise ValueError(f"Data interface not found in this {device} device.")
        return interface

    def get_client_os(self,
                      device: str):
        """
        Get OS name of the specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        device_id = self.__get_device_id(device)
        command = "shell uname"
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        return output

    def set_client_radio_state(self,
                               device: str,
                               state: int):
        """
        Enable/Disable wifi radio in client
        """
        zi_logger.print_context()
        device_id = self.__get_device_id(device)
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        if state == 1:
            command = "shell svc wifi enable"
        else:
            command = "shell svc wifi disable"
        
        zi_logger.log(f"Executing Command:{command}")
        error = connection_obj.execute_command(device_id=device_id,
                                               command=command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")

    def get_client_radio_state(self,
                               device: str) -> int:
        """
        Get client current radio state
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        device_id = self.__get_device_id(device)
        awk_expr = "awk '{print $3}'"
        command = f'shell dumpsys wifi | grep "Wi-Fi is" | {awk_expr}'
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")

        if output.lower() == 'enabled':
            return 1
        elif output.lower() == 'disabled':
            return 0

    def get_client_ipv4(self,
                        device: str) -> str:
        """
        Get IPV4 address of the given client device.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        awk_expr = "awk '{print $2}' | cut -d: -f2"
        cmd = f"shell ifconfig {interface} | grep 'inet addr' | {awk_expr}"
        zi_logger.log(f"command: {cmd}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=cmd,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {cmd}")
        return output

    def get_client_mac(self,
                       device: str) -> str:
        """
        Get MAC address of the given client device.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        awk_expr = "awk '{print $5}'"
        cmd = f"shell ifconfig {interface} | grep 'HWaddr' | {awk_expr}"
        zi_logger.log(f"command: {cmd}")        
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=cmd,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {cmd}")
        return output

    def get_client_encryption(self,
                              device: str) -> str:
        """
        Retrieve the encryption of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        cmd = (
            f"shell wpa_cli -i {interface} status | "
            "grep 'key_mgmt' | cut -d= -f2")
        zi_logger.log(f"command: {cmd}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=cmd,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return str(output)

    def get_client_frequency(self,
                             device: str) -> int:
        """
        Retrieve the frequency of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        cmd = (f"shell wpa_cli -i {interface} status | "
               "grep '^freq=' | cut -d= -f2")
        zi_logger.log(f"command: {cmd}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=cmd,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return output

    def get_client_connected_ssid(self,
                                  device: str) -> str:
        """
        Retrieve the SSID to which the client device connected currently.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        cmd = f"shell wpa_cli -i {interface} status | grep '^ssid=' | cut -d= -f2"
        zi_logger.log(f"command: {cmd}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=cmd,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or " \
            "unable to determine connection status.")
        return ast.literal_eval(f"b'{output}'").decode('utf-8')

    def get_client_connected_bssid(self,
                                   device: str) -> str:
        """
        Retrieve the BSSID of the AP to which the client device is currently connected.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        cmd = (f"shell wpa_cli -i {interface} status |"
               "grep '^bssid=' | cut -d= -f2")
        zi_logger.log(f"command: {cmd}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=cmd,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return output

    def get_client_rssi(self,
                        device: str) -> str:
        """
        Retrieve the RSSI value of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        awk_expr = "awk '{print $2}'"
        command = f"shell iw dev {interface} link | grep signal | {awk_expr}"
        zi_logger.log(f"command: {command}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return f"{str(output)}dBm"

    def get_client_channel(self,
                           device: str) -> int:
        """
        Retrieve the channel of the currently connected WiFi network on the
        specified device.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        awk_expr = '{print$2; exit}'
        command = (f"shell iw dev {interface} info | "
                   f"grep -i 'channel' | awk '{awk_expr}'")
        zi_logger.log(f"command: {command}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable" \
                             " to determine connection status.")
        return int(output)

    def get_client_bandwidth(self,
                             device: str) -> str:
        """
        Retrieve the bandwidth of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)  
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        awk_expr = '{split($2, a, ","); print a[1]}'
        command = (
            f"shell iw dev {interface} info | "
            f"awk -F'width: ' '/width/ {awk_expr}'")
        zi_logger.log(f"command: {command}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return str(output)

    def disconnect_wifi_client(self,
                               device: str):
        """
        Disconnect the wifi client from the currently connected wireless network.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        command = f"shell wpa_cli -i {interface} disconnect"
        zi_logger.log(f"command: {command}")
        error = connection_obj.execute_command(device_id=device_id,
                                               command=command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise ValueError(f"Error: Device '{interface}' is not active." \
                             f"Failed to disconnect device '{interface}'")
    
    def __interface_should_exists(self,
                                  device: str,
                                  interface: str):
        """
        Check interface should exists given device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        device_id = self.__get_device_id(device)
        command = f"shell ip link show {interface}"
        zi_logger.log(f"command: {command}")
        error = connection_obj.execute_command(device_id=device_id,
                                               command=command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise ValueError(f"{interface} Not found in this device: {device}")

    def set_client_interface_state(self,
                                   device: str,
                                   state: int):
        """
        Enable/Disable interface in client
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        self.__interface_should_exists(device, interface)
        
        if state == 1:
            command = f"ifconfig {interface} up"
        else:
            command = f"ifconfig {interface} down"
        zi_logger.log(f"command: {command}")
        error = connection_obj.execute_command(device_id=device_id,
                                               command=command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")

    def get_client_interface_state(self,
                                   device: str) -> int:
        """
        Get current interface status
        """
        zi_logger.print_context()
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        self.__interface_should_exists(device, interface)

        status = self.__check_interface_status(device,
                                              interface).lower()
        
        if status == 'up':
            return 1
        elif status == 'down':
            return 0


    def __check_interface_status(self,
                                 device: str,
                                 interface: str) -> str:
        """
        Status of radio interface default wifi interface.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        command = f"ifconfig -a {interface} | awk '/UP/ {{print 'up'}}'"
        device_id = self.__get_device_id(device)
        zi_logger.log(f"command: {command}")    
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command exection failed: {command}")
        
        if output:
            return output
        else:
            return "down"

    def check_ap_ssid_visibility(self,
                                 device: str,
                                 ssid: str) -> str:
        """
        Check the ssid of AP availablity in client
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        #status = self.__check_radio_status(device).lower()
        #status = None #This line has to be modified
        #if status != "enabled":
        #    raise Exception(
        #        "Radio interface is not enabled. " \
        #        "Please use the keyword 'Enable Radio In Client  <device>'")
        command = f"shell iw dev {interface} scan | grep 'SSID: {ssid}'"
        zi_logger.log(f"command: {command}")

        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        
        match = re.match(r"SSID:\s*(.+)", output)
        if not match:
            raise Exception(f"SSID - {ssid} is not visible")
        return match.group(1)

    def get_ap_bssid_visibility(self,
                                device: str,
                                ssid: str) -> str:
        """
        Retrieve the BSSID for the given SSID.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        #status = self.__check_radio_status(device).lower()
        #status = None #This line has to be modified
        #if status != "enabled":
        #    raise Exception("Radio interface is not enabled. " \
        #    "Please use the keyword 'Enable Radio Interface <device>'.")
        expr_1 = '/^BSS/ { split($2, mac, "\\\\("); bssid = mac[1] }'
        expr_2 = '/SSID: / { if ($2 == ssid) print bssid }'
        command = f'shell iw dev {interface} scan | awk -v ssid="{ssid}" \'{expr_1} {expr_2}\''

        zi_logger.log(f"command: {command}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        return output

    def connect_client_to_ssid(self,
                               device: str,
                               ssid: str,
                               password: str = None,
                               hidden:str = False):
        """
        Connect the client to a specified WiFi SSID.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)

        commands = [
            f"NET_ID=$(wpa_cli -i {interface} add_network)",
            f"wpa_cli -i {interface} set_network $NET_ID ssid \\\"{ssid}\\\"",
            f"wpa_cli -i {interface} set_network $NET_ID key_mgmt "
            f"{'WPA-PSK' if password is not None else 'NONE'}",
            f"wpa_cli -i {interface} set_network $NET_ID "
            f"psk \\\"{password}\\\"" if password else "",
            f"wpa_cli -i {interface} set_network $NET_ID scan_ssid 1" if hidden else "",
            f"wpa_cli -i {interface} enable_network $NET_ID",
            f"wpa_cli -i {interface} select_network $NET_ID",
            f"wpa_cli -i {interface} save_config"
        ]

        command = "shell '" + "; ".join(filter(None, commands)) + "'"
        zi_logger.log(f"command: {command}")
        error = connection_obj.execute_command(device_id=device_id,
                                               command=command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise Exception(f"Command execution failed: {command}" \
                            f"Error: {error}")
        time.sleep(5)

    def __get_connection_id(self,
                            device: str,
                            interface: str) -> int:
        """
        Get Current wifi connection id.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        device_id = self.__get_device_id(device)
        command = f"shell wpa_cli -i {interface} status | grep '^id=' | cut -d= -f2"
        zi_logger.log(f"command: {command}")
        output, error = connection_obj.execute_command(device_id=device_id,
                                                       command=command,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed: {command}" \
                            f"Error: {error}")
        return int(output)

    def remove_client_connection(self,
                                 device: str,
                                 connection_name=None):
        """
        Remove the current connection based on name assigned to the connection.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        id = self.__get_connection_id(device, interface)
        command = f'shell "cmd wifi forget-network {id}"'
        zi_logger.log(f"command: {command}")
        error = connection_obj.execute_command(device_id=device_id,
                                               command=command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise RuntimeError(f"Failed to delete: {id}")

    def __number_of_saved_networks(self,
                                   device: str) -> int:
        """
        Get the value saved networks

        -``device_id``: Specified a given adb device.
        -``returns``: Return the number of saved networks

        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        command = (
            "shell cat /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml | "
            "grep '<WifiConfiguration>' | wc -l"
        )
        device_id = self.__get_device_id(device)
        zi_logger.log(f"command: {command}")
        connections = 20
        output = connection_obj.execute_command(device_id=device_id,
                                                command=command)
        output = int(output) + connections

        if not output:
            raise RuntimeError(f"Command execution failed")
        return output
    
    def remove_all_wifi_connections(self,
                                    device: str):
        """
        Remove all wifi connections based on device.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        
        interface = self.__get_interface(device)
        device_id = self.__get_device_id(device)
        networks = self.__number_of_saved_networks(device)

        for network in range(networks):
            command = f"shell 'cmd wifi forget-network {network}'"
            zi_logger.log(f"command: {command}")
            output = connection_obj.execute_command(device_id=device_id,
                                                    command=command,
                                                    return_stdout=True,
                                                    return_stderr=True)
            if not output:
                raise RuntimeError(f"Failed to delete network {network}: {output}")
