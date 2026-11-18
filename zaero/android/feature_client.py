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
Android implementation of the client methods, using adb shell commands
(svc, dumpsys, wpa_cli, iw, ifconfig).

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
    """
    Client methods for Android devices. Each device needs a ``device_id``
    (the ADB serial number) and a ``data_iface`` in the config.
    """

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log("android.feature_client.FeatureClient.__init__ : END")

    def __get_device_id(self, device: str) -> str:
        """
        Get the ``device_id`` (ADB serial number) of the device from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the device id

        - ``Raises`` ValueError if it is empty
        """
        zi_logger.print_context()
        device_id = self.db_obj.read_from_database(device, 'device_id')
        zi_logger.log(f"device_id={device_id}")
        if not device_id:
            raise ValueError(f"Device id  not found in this {device} device.")
        return device_id

    def __get_interface(self,
                        device: str) -> str:
        """
        Get the ``data_iface`` of the device from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the interface name

        - ``Raises`` ValueError if it is empty
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
        Get the OS name of the device.

        Runs ``adb -s <device_id> shell uname``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the OS name, e.g. ``Linux``

        - ``Raises`` Exception if the command fails
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
        Turn the WiFi radio on or off.

        Runs ``adb -s <device_id> shell svc wifi enable|disable``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``state`` is ``1`` to turn the radio on, any other value turns it off

        - ``Raises`` Exception if the command fails
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
        Get the WiFi radio state.

        Runs ``adb -s <device_id> shell dumpsys wifi``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` ``1`` if enabled, ``0`` if disabled

        - ``Raises`` Exception if the command fails
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
        Get the IPv4 address of the ``data_iface``.

        Runs ``adb -s <device_id> shell ifconfig <iface>``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the IPv4 address as a string

        - ``Raises`` Exception if the command fails
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
        Get the MAC address of the ``data_iface``.

        Runs ``adb -s <device_id> shell ifconfig <iface>``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the MAC address as a string

        - ``Raises`` Exception if the command fails
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
        Get the key management of the connected WiFi network.

        Runs ``adb -s <device_id> shell wpa_cli -i <iface> status``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the ``key_mgmt`` value, e.g. ``WPA2-PSK``

        - ``Raises`` ValueError if the command fails
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
        Get the frequency of the connected WiFi network.

        Runs ``adb -s <device_id> shell wpa_cli -i <iface> status``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the frequency in MHz as a string

        - ``Raises`` ValueError if the command fails
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
        Get the SSID the device is connected to.

        Runs ``adb -s <device_id> shell wpa_cli -i <iface> status``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the SSID, with escaped bytes decoded as UTF-8

        - ``Raises`` ValueError if the command fails
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
        Get the BSSID of the access point the device is connected to.

        Runs ``adb -s <device_id> shell wpa_cli -i <iface> status``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the BSSID as a string

        - ``Raises`` ValueError if the command fails
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
        Get the signal strength of the connected WiFi network.

        Runs ``adb -s <device_id> shell iw dev <iface> link``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the signal as a string, e.g. ``-45dBm``

        - ``Raises`` ValueError if the command fails
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
        Get the channel of the connected WiFi network.

        Runs ``adb -s <device_id> shell iw dev <iface> info``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the channel number as an integer

        - ``Raises`` ValueError if the command fails
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
        Get the channel width of the connected WiFi network.

        Runs ``adb -s <device_id> shell iw dev <iface> info``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the channel width as a string, e.g. ``80 MHz``

        - ``Raises`` ValueError if the command fails
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
        Disconnect the device from its WiFi network.

        Runs ``adb -s <device_id> shell wpa_cli -i <iface> disconnect``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` ValueError if the command fails
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
        Check that the interface exists, with ``adb shell ip link show``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the interface name

        - ``Raises`` ValueError if the interface does not exist
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
        Bring the ``data_iface`` up or down.

        Runs ``adb -s <device_id> ifconfig <iface> up|down``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``state`` is ``1`` for up, any other value for down

        - ``Raises`` ValueError if the interface does not exist, Exception if the command fails
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
        Get the state of the ``data_iface``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` ``1`` if up, ``0`` if down

        - ``Raises`` ValueError if the interface does not exist
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
        Get whether the interface is up, from ``ifconfig -a``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the interface name

        - ``Returns`` the command output if the interface is up, else ``down``

        - ``Raises`` Exception if the command fails
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
        Check that the SSID appears in the WiFi scan.

        Runs ``adb -s <device_id> shell iw dev <iface> scan``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to look for

        - ``Returns`` the SSID found in the scan

        - ``Raises`` Exception if the command fails or the SSID is not visible
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
        Get the BSSID of the access points broadcasting the SSID, from the WiFi scan.

        Runs ``adb -s <device_id> shell iw dev <iface> scan``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to look for

        - ``Returns`` the BSSID of each matching scan entry, one per line

        - ``Raises`` Exception if the command fails
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
        Add a WiFi network with ``wpa_cli``, select it and save the config, then wait 5 seconds.

        Runs ``adb -s <device_id> shell 'wpa_cli -i <iface> add_network; ...'``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to connect to

        - ``password`` is the WPA-PSK password, or None for an open network

        - ``hidden`` True if the SSID is hidden (sets ``scan_ssid 1``)

        - ``Raises`` Exception if the command fails
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
        Get the network id of the current WiFi connection from
        ``wpa_cli -i <iface> status``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the WiFi interface name

        - ``Returns`` the network id as an integer

        - ``Raises`` Exception if the command fails
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
        Forget the currently connected WiFi network.

        Runs ``adb -s <device_id> shell "cmd wifi forget-network <id>"``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``connection_name`` is not used; the current connection is always removed

        - ``Raises`` RuntimeError if the network could not be forgotten
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
        Get the number of network ids to forget: the number of saved networks
        in ``WifiConfigStore.xml`` plus 20.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the number of network ids

        - ``Raises`` RuntimeError if the result is 0
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
        Forget all saved WiFi networks, trying each network id in turn.

        Runs ``adb -s <device_id> shell 'cmd wifi forget-network <id>'``; ``device_id`` and ``data_iface`` are read from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` RuntimeError if a command returns no output
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
