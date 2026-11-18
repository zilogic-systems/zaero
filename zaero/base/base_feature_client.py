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
Abstract base class for WiFi and LAN client methods.

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod


class BaseFeatureClient(ABC):
    """
    Abstract methods a platform plugin implements for WiFi and LAN client.
    Implemented by zaero.linux and zaero.android.
    """
    @abstractmethod
    def get_client_os(self,
                      device: str):
        """
        Get the OS name of the client device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the OS name

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_os()")
        
    @abstractmethod
    def get_client_ipv4(self,
                        device: str):
        """
        Get the IPv4 address of the client device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the IPv4 address

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_ipv4()")

    @abstractmethod
    def set_client_radio_state(self,
                               device:str,
                               state:int):
        """
        Turn the WiFi radio of the client on (``state`` 1) or off (``state`` 0).

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``state`` is the desired state

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement set_client_radio_state()")
    
    @abstractmethod
    def get_client_radio_state(self,
                               device:str):
        """
        Get the WiFi radio state of the client.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` ``1`` if enabled, ``0`` if disabled

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_radio_state()")
    
    @abstractmethod
    def set_client_interface_state(self,
                                   device: str,
                                   state: str):
        """
        Bring the data interface of the client up (``state`` 1) or down (``state`` 0).

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``state`` is the desired state

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement set_client_interface_state()")

    @abstractmethod
    def get_client_interface_state(self,
                                   device: str):
        """
        Get the state of the data interface of the client.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` ``1`` if up, ``0`` if down

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_interface_state()")
        
    @abstractmethod
    def check_ap_ssid_visibility(self,
                                 device: str,
                                 ssid: str):
        """
        Check that the SSID is visible in the WiFi scan of the client. Raise an exception if not.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_ssid_availability_in_client()")
        
    @abstractmethod
    def get_ap_bssid_visibility(self,
                                device: str,
                                ssid: str):
        """
        Get the BSSID of the access point broadcasting the SSID, from the WiFi scan of the client.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID

        - ``Returns`` the BSSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_ap_bssid_visibility()")                                 
        
    @abstractmethod
    def connect_client_to_ssid(self,
                               device: str,
                               ssid: str,
                               password: str,
                               hidden:str):
        """
        Connect the client to the WiFi network.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``ssid`` is the SSID

        - ``password`` is the WiFi password, or None for an open network

        - ``hidden`` True if the SSID is hidden

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement connect_client_to_ssid()")    
        
    @abstractmethod
    def get_client_connected_ssid(self,
                                  device: str):
        """
        Get the SSID the client is connected to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the SSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_connected_ssid()") 

    @abstractmethod
    def get_client_channel(self,
                           device: str):
        """
        Get the channel of the WiFi network the client is connected to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the channel number

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_channel()")
        
    @abstractmethod
    def remove_client_connection(self,
                                 device: str,
                                 connection: str):
        """
        Delete a saved connection on the client.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``connection`` is the name of the saved connection, normally the SSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement remove_client_connection()")
        
    @abstractmethod
    def remove_all_wifi_connections(self,
                                    device: str):
        """
        Delete all saved WiFi connections on the client.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement remove_all_wifi_connections()")
        
    @abstractmethod
    def get_client_bandwidth(self,
                             device: str):
        """
        Get the channel width of the WiFi network the client is connected to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the channel width

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_bandwidth()")
        
    @abstractmethod
    def get_client_encryption(self,
                              device: str):
        """
        Get the key management of the WiFi network the client is connected to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the key management, e.g. ``WPA2-PSK``

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_encryption()")

    @abstractmethod
    def get_client_frequency(self,
                                device: str):
        """
        Get the frequency of the WiFi network the client is connected to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the frequency in MHz

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_frequency()")

    @abstractmethod
    def get_client_rssi(self,
                        device: str):
        """
        Get the signal strength of the WiFi network the client is connected to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the signal strength

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_client_rssi()")

    @abstractmethod
    def disconnect_wifi_client(self,
                               device: str):
        """
        Disconnect the client from its WiFi network.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement disconnect_wifi_client()")
