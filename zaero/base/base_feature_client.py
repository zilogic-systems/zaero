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
This module handles client abstract method

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod


class BaseFeatureClient(ABC):
    """ This module provide abstract class for the APIs in client"""
    @abstractmethod
    def get_client_os(self,
                      device: str):
        """ Get os in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_os()")
        
    @abstractmethod
    def get_client_ipv4(self,
                        device: str):
        """ Get ipv4 in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_ipv4()")

    @abstractmethod
    def set_client_radio_state(self,
                               device:str,
                               state:int):
        """ Enable/Disable radio in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement set_client_radio_state()")
    
    @abstractmethod
    def get_client_radio_state(self,
                               device:str):
        """ Retrieve the radio state in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_radio_state()")
    
    @abstractmethod
    def set_client_interface_state(self,
                                   device: str,
                                   state: str):
        """ Enable/Disable wifi interface in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement set_client_interface_state()")

    @abstractmethod
    def get_client_interface_state(self,
                                   device: str):
        """Retrieve wifi interface state in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_interface_state()")
        
    @abstractmethod
    def check_ap_ssid_visibility(self,
                                 device: str,
                                 ssid: str):
        """ Check ap ssid visibility in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_ssid_availability_in_client()")
        
    @abstractmethod
    def get_ap_bssid_visibility(self,
                                device: str,
                                ssid: str):
        """ Get Bssid Availablity in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_ap_bssid_visibility()")                                 
        
    @abstractmethod
    def connect_client_to_ssid(self,
                               device: str,
                               ssid: str,
                               password: str,
                               hidden:str):
        """ Connect to ssid in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement connect_client_to_ssid()")    
        
    @abstractmethod
    def get_client_connected_ssid(self,
                                  device: str):
        """ Get Connected ssid in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_connected_ssid()") 

    @abstractmethod
    def get_client_channel(self,
                           device: str):
        """ Get Channel in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_channel()")
        
    @abstractmethod
    def remove_client_connection(self,
                                 device: str,
                                 connection: str):
        """ Remove connection in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement remove_client_connection()")
        
    @abstractmethod
    def remove_all_wifi_connections(self,
                                    device: str):
        """ Remove all wifi connection in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement remove_all_wifi_connections()")
        
    @abstractmethod
    def get_client_bandwidth(self,
                             device: str):
        """ Get bandwidth in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_bandwidth()")
        
    @abstractmethod
    def get_client_encryption(self,
                              device: str):
        """ Get encryption in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_encryption()")

    @abstractmethod
    def get_client_frequency(self,
                                device: str):
        """ Get frequency in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_frequency()")

    @abstractmethod
    def get_client_rssi(self,
                        device: str):
        """ Get signal strength in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement get_client_rssi()")

    @abstractmethod
    def disconnect_wifi_client(self,
                               device: str):
        """ Disconnect wifi in client abstract method"""
        raise NotImplementedError(
            "Subclass must implement disconnect_wifi_client()")
