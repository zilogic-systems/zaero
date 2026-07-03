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
This module handles Linux WiFi client operations
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
    """Handles basic WiFi functionality keywords for Linux client."""
    
    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log("Linux.FeatureClient __init__ : END")

    def get_client_os(self,
                      device) -> str:
        """
        Get The Operating system.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        output, error = connection_obj.execute_command("uname",
                                                       return_stderr = True)
        if error != '':
            raise Exception(f"Command execution failed : uname")
        return output
    
    def __get_interface(self,
                        device: str) -> str:
        """
        Get interface of the specified device.
        """
        zi_logger.print_context()
        try:
            interface = self.db_obj.read_from_database(device, 'data_iface')
            zi_logger.log(f"Data interface: {interface}")
            zi_logger.log("Feature: Client")
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            zi_logger.log(f"Could not find out the Radio of the device : {device}","error")
        return interface
    
    def get_client_ipv4(self,
                        device: str) -> str:
        """
        Get The IPv4 address from given interface.
        """
        zi_logger.print_context()
        interface = self.db_obj.read_from_database(device, 'data_iface')
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        zi_logger.log(connection_obj)
        connection_obj.switch_connection(device)
        command = f"/sbin/ifconfig {interface} | grep 'inet ' | cut -d' ' -f10"
        output, error = connection_obj.execute_command(command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        zi_logger.log(f"output: {output}, error: {error}")
        if error:
            raise Exception(f"Command execution failed : {command}")
        return output

    def __interface_should_exists(self,
                                  device: str,
                                  interface: str) -> bool:
        """
        Check interface should exists given device.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        command = f"/usr/sbin/ip link show {interface}"
        error = connection_obj.execute_command(command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            return False
        return True

    
    def __get_interface_type(self,
                             device,
                             interface: str) ->  str:
        """
        Retrieve the type of a network interface, such as wifi/ethernet.
        """
        zi_logger.print_context()
        is_available = self.__interface_should_exists(device,
                                                     interface)

        if not is_available:
            raise ValueError(f"Interface Error: {interface} is not Found")

        awk_expr = '{print $2}'
        command = (
            f"nmcli device show {interface} | "
            f"awk -F': +' '/GENERAL.TYPE/ {awk_expr}'")
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        output = connection_obj.execute_command(command,
                                                return_stdout=True)
        if not output:
            raise Exception(f"Command exection failed: {command}")
        return output

    
    def __check_interface_status(self,
                                 device: str,
                                 interface: str) -> str:
        """
        Status of radio interface default wifi interface.
        """
        zi_logger.print_context()
        command = (
            f"ifconfig {interface} | grep flags | "
            "awk -F'[<>]' '{split($2,a,\",\"); print a[1]}'")
        
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        output, error = connection_obj.execute_command(command,
                                                       return_stdout=True,
                                                       return_stderr=True)

        if error:
            raise Exception(f"Command exection failed: {command}")
        if output=='UP':
            return "up"
        else:
            return "down"

    
    def set_client_radio_state(self,
                               device: str,
                               state: int):
        """
        Enable/Disable wifi radio in client
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        if state == 1:
            command = "nmcli radio wifi on"
        else:
            command = "nmcli radio wifi off"

        error = connection_obj.execute_command(command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")

    
    def get_client_radio_state(self,
                             device: str) -> int:
        """
        Check current radio status
        """
        zi_logger.print_context()
        command = "nmcli radio wifi"
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        output, error = connection_obj.execute_command(command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        
        output = output.lower()

        if output == 'enabled':
            return 1
        elif output == 'disabled':
            return 0

    
    def set_client_interface_state(self,
                                   device: str,
                                   state: int):
        """
        Enable/Disable interface in client
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        interface = self.db_obj.read_from_database(device, 'data_iface')
        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type not in ["wifi", "ethernet"]:
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi/Ethernet interface")

        if state == 1:
            command = f"ifconfig {interface} up"
        else:
            command = f"ifconfig {interface} down"

        error = connection_obj.execute_command(command,
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
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        interface = self.db_obj.read_from_database(device, 'data_iface')
        conn_type = self.__get_interface_type(device,
                                                interface).lower()

        if conn_type not in ["wifi", "ethernet"]:
            raise ValueError(f"Interface Error: {interface} " \
                                "is not a WiFi/Ethernet interface")
        status = self.__check_interface_status(device,
                                                interface).lower()
        
        if status == 'up':
            return 1
        elif status == 'down':
            return 0

    
    def check_ap_ssid_visibility(self,
                                 device: str,
                                 ssid: str) -> str:
        """
        Check the ssid of AP availablity in client
        """
        zi_logger.print_context()
        status = self.get_client_radio_state(device)
        if not status:
            raise Exception(
                "Radio interface is not enabled. " \
                "Please use the keyword 'Enable Radio In Client  <device>'")
        
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        awk_expr = '{if ($1 == "*") print $3; else print $2}'
        command = (
            "nmcli device wifi list | "
            f"grep -im1 ' {ssid} ' | "
            f"awk '{awk_expr}'")

        output, error = connection_obj.execute_command(command,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        if output != ssid:
            raise Exception(f"SSID - {ssid} is not visible")

    
    def get_ap_bssid_visibility(self,
                                device: str,
                                ssid: str) -> str:
        """
        Retrieve the BSSID for the given SSID.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)

        status = self.get_client_radio_state(device)
        if not status:
            raise Exception("Radio interface is not enabled. " \
            "Please use the keyword 'Enable Radio Interface <device>'.")
        awk_expr = '{if ($1 == "*") print $3; else print $2}'
        command = (
            "nmcli device wifi list | "
            f"grep -im1 ' {ssid} ' | "
            f"awk '{awk_expr}'")
        output, error = connection_obj.execute_command(command,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")

        bssid_match = re.search(r'([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}', output)

        if bssid_match:
            return bssid_match.group()

    
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
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        cmd_parts = [
            "nmcli device wifi connect",
            f'"{ssid}"',
            f"password '{password}'" if password is not None else "",
            f"ifname {interface}",
            "hidden yes" if hidden else ""
            ]
        filter_cmd_parts = list(filter(None, cmd_parts))
        command = " ".join(filter_cmd_parts)

        error = connection_obj.execute_command(command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise Exception(f"Command execution failed: {command}" \
                            f"Error: {error}")

    
    def get_client_connected_ssid(self,
                                  device: str) -> str:
        """
        Retrieve the SSID to which the client device connected currently.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')
        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        awk_expr = '{print$2}'
        command = f"iw dev {interface} link | grep 'SSID' | awk '{awk_expr}'"
        output, error = connection_obj.execute_command(command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or " \
            "unable to determine connection status.")
        return ast.literal_eval(f"b'{output}'").decode('utf-8')

    
    def get_client_channel(self,
                           device: str) -> int:
        """
        Retrieve the channel of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        awk_expr = '{print$2; exit}'
        command = (f"iw dev {interface} info | "
                   f"grep -i 'channel' | awk '{awk_expr}'")
        output, error = connection_obj.execute_command(command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable" \
                             " to determine connection status.")
        return int(output)

    
    def remove_client_connection(self,
                                 device: str,
                                 connection_name: str):
        """
        Remove the connection based on name assigned to the connection_obj.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if not conn_type in ['ethernet', 'wifi']:
            raise TypeError(f"Invalid {conn_type} connections detected")

        command =  f"nmcli connection show | grep '{connection_name}'"

        output = connection_obj.execute_command(command,
                                                return_stdout=True)
        if output:
            command = f"nmcli connection delete '{connection_name}'"
            error = connection_obj.execute_command(command,
                                                   return_stdout=False,
                                                   return_stderr=True)
            if error:
                raise RuntimeError(f"Failed to delete: {connection_name}")

    
    def remove_all_wifi_connections(self,
                                   device: str):
        """
        Remove all wifi connections based on device.
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != 'wifi':
            raise TypeError(f"Invalid {conn_type} connections detected")

        list_uuid_cmd = ("nmcli -f UUID,TYPE,DEVICE connection show |"
                         f"grep '{conn_type}' | awk '{{print $1}}'")
        
        uuids = connection_obj.execute_command(list_uuid_cmd,
                                               return_stdout=True)

        if not uuids:
            zi_logger.log(f"No {conn_type} connections found.")
            return

        for uuid in uuids.strip().splitlines():
            delete_cmd = f"nmcli connection delete uuid {uuid.strip()}"
            error = connection_obj.execute_command(delete_cmd,
                                                   return_stdout=False,
                                                   return_stderr=True)
            if error:
                raise RuntimeError(f"Failed to delete UUID {uuid}: {error}")

    
    def get_client_bandwidth(self,
                             device: str) -> str:
        """
        Retrieve the bandwidth of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        awk_expr = '{split($2, a, ","); print a[1]}'
        command = (
            f"iw dev {interface} info | "
            f"awk -F'width: ' '/width/ {awk_expr}'")

        output, error = connection_obj.execute_command(command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return str(output)

    
    def get_client_encryption(self,
                              device: str) -> str:
        """
        Retrieve the encryption of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = (
            f"wpa_cli -i {interface} status | "
            "grep 'key_mgmt' | cut -d= -f2"
        )
        output, error = connection_obj.execute_command(command,
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
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = (
            f"iw dev {interface} link | grep 'freq' | "
            "cut -d: -f2 | tr -d ' '")
        output, error = connection_obj.execute_command(command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return int(float(output))

    
    def get_client_rssi(self,
                        device: str) -> str:
        """
        Retrieve the RSSI value of the currently connected WiFi network on the
        specified device
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = (
            f"iw dev {interface} link | grep 'signal' | "
            "cut -d: -f2 | tr -d ' '")
        output, error = connection_obj.execute_command(command,
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
        connection_obj.switch_connection(device)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = f"nmcli device disconnect {interface}"
        error = connection_obj.execute_command(command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise ValueError(f"Error: Device '{interface}' is not active.")
        
        command = f"nmcli device status | grep ' {conn_type} ' | awk '{{print $3}}'"
        output = connection_obj.execute_command(command,
                                                return_stdout=True,
                                                return_stderr=False)
        zi_logger.log(output)
        if output != 'disconnected':
            raise ValueError(f"Failed to disconnect device '{interface}'")
    
