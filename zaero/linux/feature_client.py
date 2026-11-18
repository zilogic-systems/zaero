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
Linux implementation of the client methods, using nmcli, iw, wpa_cli
and ifconfig over the device connection.

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
    Client methods for Linux hosts. The interface used is ``data_iface`` from the config.
    """
    
    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log("Linux.FeatureClient __init__ : END")

    def get_client_os(self,
                      device) -> str:
        """
        Get the OS name of the device with ``uname``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the OS name, e.g. ``Linux``

        - ``Raises`` Exception if the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        output, error = connection_obj.execute_command(device, "uname",
                                                       return_stderr = True)
        if error != '':
            raise Exception(f"Command execution failed : uname")
        return output
    
    def __get_interface(self,
                        device: str) -> str:
        """
        Get the ``data_iface`` of the device from the config.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the interface name
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
        Get the IPv4 address of the ``data_iface`` with ``ifconfig``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the IPv4 address as a string

        - ``Raises`` Exception if the command fails
        """
        zi_logger.print_context()
        interface = self.db_obj.read_from_database(device, 'data_iface')
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        zi_logger.log(connection_obj)
        command = f"/sbin/ifconfig {interface} | grep 'inet ' | cut -d' ' -f10"
        output, error = connection_obj.execute_command(device, command,
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
        Check whether the interface exists, with ``ip link show``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the interface name

        - ``Returns`` True if it exists, False otherwise
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        command = f"/usr/sbin/ip link show {interface}"
        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            return False
        return True

    
    def __get_interface_type(self,
                             device,
                             interface: str) ->  str:
        """
        Get the type of the interface from ``nmcli device show``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the interface name

        - ``Returns`` the type, e.g. ``wifi`` or ``ethernet``

        - ``Raises`` ValueError if the interface does not exist, Exception if the
          type could not be read
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
        output = connection_obj.execute_command(device, command,
                                                return_stdout=True)
        if not output:
            raise Exception(f"Command exection failed: {command}")
        return output

    
    def __check_interface_status(self,
                                 device: str,
                                 interface: str) -> str:
        """
        Get whether the interface is up, from the flags shown by ``ifconfig``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the interface name

        - ``Returns`` ``up`` or ``down``

        - ``Raises`` Exception if the command fails
        """
        zi_logger.print_context()
        command = (
            f"ifconfig {interface} | grep flags | "
            "awk -F'[<>]' '{split($2,a,\",\"); print a[1]}'")
        
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        output, error = connection_obj.execute_command(device, command,
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
        Turn the WiFi radio on or off with ``nmcli radio wifi on|off``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``state`` is ``1`` to turn the radio on, any other value turns it off

        - ``Raises`` Exception if the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        if state == 1:
            command = "nmcli radio wifi on"
        else:
            command = "nmcli radio wifi off"

        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")

    
    def get_client_radio_state(self,
                             device: str) -> int:
        """
        Get the WiFi radio state with ``nmcli radio wifi``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` ``1`` if enabled, ``0`` if disabled

        - ``Raises`` Exception if the command fails
        """
        zi_logger.print_context()
        command = "nmcli radio wifi"
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        output, error = connection_obj.execute_command(device, command,
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
        Bring the ``data_iface`` up or down with ``ifconfig``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``state`` is ``1`` for up, any other value for down

        - ``Raises`` ValueError if the interface is missing or is not a WiFi or
          Ethernet interface, Exception if the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        interface = self.db_obj.read_from_database(device, 'data_iface')
        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type not in ["wifi", "ethernet"]:
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi/Ethernet interface")

        if state == 1:
            command = f"ifconfig {interface} up"
        else:
            command = f"ifconfig {interface} down"

        error = connection_obj.execute_command(device, command,
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

        - ``Raises`` ValueError if the interface is missing or is not a WiFi or
          Ethernet interface
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

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
        Check that the SSID appears in ``nmcli device wifi list``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to look for

        - ``Raises`` Exception if the radio is off, the command fails or the
          SSID is not visible
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

        output, error = connection_obj.execute_command(device, command,
                                                       return_stderr=True)
        if error:
            raise Exception(f"Command execution failed : {command}")
        if output != ssid:
            raise Exception(f"SSID - {ssid} is not visible")

    
    def get_ap_bssid_visibility(self,
                                device: str,
                                ssid: str) -> str:
        """
        Get the BSSID of the first ``nmcli device wifi list`` entry that matches
        the SSID.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to look for

        - ``Returns`` the BSSID, or None if no MAC address is found

        - ``Raises`` Exception if the radio is off or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        status = self.get_client_radio_state(device)
        if not status:
            raise Exception("Radio interface is not enabled. " \
            "Please use the keyword 'Enable Radio Interface <device>'.")
        awk_expr = '{if ($1 == "*") print $3; else print $2}'
        command = (
            "nmcli device wifi list | "
            f"grep -im1 ' {ssid} ' | "
            f"awk '{awk_expr}'")
        output, error = connection_obj.execute_command(device, command,
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
                               bssid: str = None,
                               hidden: bool = False):
        """
        Connect the ``data_iface`` to a WiFi network with
        ``nmcli device wifi connect``.

        If ``bssid`` is given, the connection is also locked to that BSSID
        (``802-11-wireless.bssid``) and restarted.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID to connect to

        - ``password`` is the WiFi password, or None for an open network

        - ``bssid`` is the BSSID to connect to, or None for any

        - ``hidden`` True if the SSID is hidden

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface,
          Exception or RuntimeError if a command fails
        """
        zi_logger.print_context()

        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)

        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} is not a WiFi interface")
        # Build nmcli command
        cmd_parts = [
            "nmcli device wifi connect",
            f'"{ssid}"',
        ]

        if password is not None:
            cmd_parts.append(f"password '{password}'")

        if bssid:
            cmd_parts.append(f"bssid {bssid.upper()}")

        cmd_parts.append(f"ifname {interface}")

        if hidden:
            cmd_parts.append("hidden yes")

        command = " ".join(cmd_parts)

        zi_logger.log(f"Connecting client using command: {command}")

        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True)

        if error:
            raise Exception(
                f"Command execution failed: {command}\n"
                f"Error: {error}"
            )
        if bssid:
            zi_logger.log(f"Locking connection to BSSID: {bssid.upper()}")
            command = (f"nmcli connection modify '{ssid}' 802-11-wireless.bssid {bssid.upper()}")
            error = connection_obj.execute_command(device, command, return_stdout=False,return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}\nError: {error}")
            command = f"nmcli connection down '{ssid}'"
            error = connection_obj.execute_command(device, command,return_stdout=False,return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}\nError: {error}")
            command = f"nmcli connection up '{ssid}'"
            error = connection_obj.execute_command(device, command,return_stdout=False,return_stderr=True)
            if error:
                raise RuntimeError(f"Command execution failed: {command}\n Error: {error}")

    
    def get_client_connected_ssid(self,
                                  device: str) -> str:
        """
        Get the SSID the device is connected to.

        Uses ``iw dev <iface> link`` on the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the SSID, with escaped bytes such as ``\\xe2`` decoded as UTF-8

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')
        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        awk_expr = '{print$2}'
        command = f"iw dev {interface} link | grep 'SSID' | awk '{awk_expr}'"
        output, error = connection_obj.execute_command(device, command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or " \
            "unable to determine connection status.")
        return ast.literal_eval(f"b'{output}'").decode('utf-8')

    
    def get_client_channel(self,
                           device: str) -> int:
        """
        Get the channel of the connected WiFi network.

        Uses ``iw dev <iface> info`` on the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the channel number as an integer

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        awk_expr = '{print$2; exit}'
        command = (f"iw dev {interface} info | "
                   f"grep -i 'channel' | awk '{awk_expr}'")
        output, error = connection_obj.execute_command(device, command,
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
        Delete a saved connection with ``nmcli connection delete``, if it is
        listed in ``nmcli connection show``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``connection_name`` is the connection name, normally the SSID

        - ``Raises`` TypeError if the ``data_iface`` is not a WiFi or Ethernet
          interface, RuntimeError if the connection could not be deleted
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if not conn_type in ['ethernet', 'wifi']:
            raise TypeError(f"Invalid {conn_type} connections detected")

        command =  f"nmcli connection show | grep '{connection_name}'"

        output = connection_obj.execute_command(device, command,
                                                return_stdout=True)
        if output:
            command = f"nmcli connection delete '{connection_name}'"
            error = connection_obj.execute_command(device, command,
                                                   return_stdout=False,
                                                   return_stderr=True)
            if error:
                raise RuntimeError(f"Failed to delete: {connection_name}")

    
    def remove_all_wifi_connections(self,
                                   device: str):
        """
        Delete all saved WiFi connections listed by ``nmcli connection show``.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` TypeError if the ``data_iface`` is not a WiFi interface,
          RuntimeError if a connection could not be deleted
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != 'wifi':
            raise TypeError(f"Invalid {conn_type} connections detected")

        list_uuid_cmd = ("nmcli -f UUID,TYPE,DEVICE connection show |"
                         f"grep '{conn_type}' | awk '{{print $1}}'")
        
        uuids = connection_obj.execute_command(device, list_uuid_cmd,
                                               return_stdout=True)

        if not uuids:
            zi_logger.log(f"No {conn_type} connections found.")
            return

        for uuid in uuids.strip().splitlines():
            delete_cmd = f"nmcli connection delete uuid {uuid.strip()}"
            error = connection_obj.execute_command(device, delete_cmd,
                                                   return_stdout=False,
                                                   return_stderr=True)
            if error:
                raise RuntimeError(f"Failed to delete UUID {uuid}: {error}")

    
    def get_client_bandwidth(self,
                             device: str) -> str:
        """
        Get the channel width of the connected WiFi network.

        Uses ``iw dev <iface> info`` on the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the channel width as a string, e.g. ``80 MHz``

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        awk_expr = '{split($2, a, ","); print a[1]}'
        command = (
            f"iw dev {interface} info | "
            f"awk -F'width: ' '/width/ {awk_expr}'")

        output, error = connection_obj.execute_command(device, command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return str(output)

    
    def get_client_encryption(self,
                              device: str) -> str:
        """
        Get the key management of the connected WiFi network.

        Uses ``wpa_cli -i <iface> status`` on the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the ``key_mgmt`` value, e.g. ``WPA2-PSK``

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = (
            f"wpa_cli -i {interface} status | "
            "grep 'key_mgmt' | cut -d= -f2"
        )
        output, error = connection_obj.execute_command(device, command,
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

        Uses ``iw dev <iface> link`` on the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the frequency in MHz as an integer

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = (
            f"iw dev {interface} link | grep 'freq' | "
            "cut -d: -f2 | tr -d ' '")
        output, error = connection_obj.execute_command(device, command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return int(float(output))

    
    def get_client_rssi(self,
                        device: str) -> str:
        """
        Get the signal strength of the connected WiFi network.

        Uses ``iw dev <iface> link`` on the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the signal as a string, e.g. ``-45dBm``

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or the command fails
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = (
            f"iw dev {interface} link | grep 'signal' | "
            "cut -d: -f2 | tr -d ' '")
        output, error = connection_obj.execute_command(device, command,
                                                       return_stdout=True,
                                                       return_stderr=True)
        if error:
            raise ValueError("Invalid interface or unable to " \
                             "determine connection status.")
        return str(output)

    
    def disconnect_wifi_client(self,
                               device: str):
        """
        Disconnect the device from its WiFi network and check that nmcli reports it as disconnected.

        Uses ``nmcli device disconnect <iface>`` on the ``data_iface`` of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` ValueError if the ``data_iface`` is not a WiFi interface or the device could not be disconnected
        """
        zi_logger.print_context()
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        interface = self.db_obj.read_from_database(device, 'data_iface')

        conn_type = self.__get_interface_type(device, interface).lower()

        if conn_type != "wifi":
            raise ValueError(f"Interface Error: {interface} " \
                             "is not a WiFi interface")

        command = f"nmcli device disconnect {interface}"
        error = connection_obj.execute_command(device, command,
                                               return_stdout=False,
                                               return_stderr=True)
        if error:
            raise ValueError(f"Error: Device '{interface}' is not active.")
        
        command = f"nmcli device status | grep ' {conn_type} ' | awk '{{print $3}}'"
        output = connection_obj.execute_command(device, command,
                                                return_stdout=True,
                                                return_stderr=False)
        zi_logger.log(output)
        if output != 'disconnected':
            raise ValueError(f"Failed to disconnect device '{interface}'")
    
