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
This module handles interface abstract methods

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod


class BaseFeatureInterface(ABC):
    """ This module provides abstract class for the APIs in interface"""

    @abstractmethod
    def set_ssid(self, device: str, index: str, ssid: str):
        """ Set SSID abstract method"""
        raise NotImplementedError("Subclass must implement set_ssid()")

    @abstractmethod
    def set_interface_from_database(self, device: str, index: str):
        """ Set interface parameters from database abstract method"""
        raise NotImplementedError("Subclass must implement set_interface_from_database()")

    @abstractmethod
    def get_interface(self, device: str, index: str):
        """ Get interface abstract method"""
        raise NotImplementedError("Subclass must implement get_interface()")

    @abstractmethod
    def check_interface(self, device: str, index: str):
        """ Check interface abstract method"""
        raise NotImplementedError("Subclass must implement check_interface()")

    @abstractmethod
    def get_ssid(self, device: str, index: str):
        """ Get SSID abstract method"""
        raise NotImplementedError("Subclass must implement get_ssid()")

    @abstractmethod
    def check_ssid(self, device: str, index: str, ssid: str):
        """ Check SSID abstract method"""
        raise NotImplementedError("Subclass must implement check_ssid()")

    @abstractmethod
    def set_encryption(self, device: str, index: str, encryption: str):
        """ Set encryption abstract method"""
        raise NotImplementedError("Subclass must implement set_encryption()")

    @abstractmethod
    def get_encryption(self, device: str, index: str):
        """ Get encryption abstract method"""
        raise NotImplementedError("Subclass must implement get_encryption()")

    @abstractmethod
    def set_password(self, device: str, index: str, password: str):
        """ Set password abstract method"""
        raise NotImplementedError("Subclass must implement set_password()")

    @abstractmethod
    def get_password(self, device: str, index: str):
        """ Get password abstract method"""
        raise NotImplementedError("Subclass must implement get_password()")

    @abstractmethod
    def set_sae_parameters(self, device: str, index: str, password: str):
        """ Set SAE parameters abstract method"""
        raise NotImplementedError("Subclass must implement set_sae_parameters()")

    @abstractmethod
    def check_brctl_show(self, device: str, bridge: str, interface: str):
        """ Check bridge control show abstract method"""
        raise NotImplementedError("Subclass must implement check_brctl_show()")

    @abstractmethod
    def get_dut_bridge_ipv4(self, device: str, bridge: str):
        """ Get DUT bridge IPv4 abstract method"""
        raise NotImplementedError("Subclass must implement get_dut_bridge_ipv4()")

    @abstractmethod
    def get_dut_wan_ipv4(self, device: str, interface: str):
        """ Get DUT WAN IPv4 abstract method"""
        raise NotImplementedError("Subclass must implement get_dut_wan_ipv4()")

    @abstractmethod
    def set_wifi_iface_device(self, device: str, index: str, radio: str):
        """ Set wifi interface device abstract method"""
        raise NotImplementedError("Subclass must implement set_wifi_iface_device()")

    @abstractmethod
    def get_wifi_iface_device(self, device: str, index: str):
        """ Get wifi interface device abstract method"""
        raise NotImplementedError("Subclass must implement get_wifi_iface_device()")

    @abstractmethod
    def set_wifi_iface_network(self, device: str, index: str, network: str):
        """ Set wifi interface network abstract method"""
        raise NotImplementedError("Subclass must implement set_wifi_iface_network()")

    @abstractmethod
    def get_wifi_iface_network(self, device: str, index: str):
        """ Get wifi interface network abstract method"""
        raise NotImplementedError("Subclass must implement get_wifi_iface_network()")

    @abstractmethod
    def set_wifi_iface_mode(self, device: str, index: str, mode: str):
        """ Set wifi interface mode abstract method"""
        raise NotImplementedError("Subclass must implement set_wifi_iface_mode()")

    @abstractmethod
    def get_wifi_iface_mode(self, device: str, index: str):
        """ Get wifi interface mode abstract method"""
        raise NotImplementedError("Subclass must implement get_wifi_iface_mode()")

    @abstractmethod
    def check_mode(self, device: str, index: str, mode: str):
        """ Check wifi interface mode abstract method"""
        raise NotImplementedError("Subclass must implement check_mode()")

    @abstractmethod
    def set_wifi_iface_isolate(self, device: str, index: str, isolate: str):
        """ Set wifi interface isolate abstract method"""
        raise NotImplementedError("Subclass must implement set_wifi_iface_isolate()")

    @abstractmethod
    def get_wifi_iface_isolate(self, device: str, index: str):
        """ Get wifi interface isolate abstract method"""
        raise NotImplementedError("Subclass must implement get_wifi_iface_isolate()")

    @abstractmethod
    def add_wifi_interface(self, device: str, index: str):
        """ Add wifi interface abstract method"""
        raise NotImplementedError("Subclass must implement add_wifi_interface()")

    @abstractmethod
    def delete_wifi_interface(self, device: str, index: str):
        """ Delete wifi interface abstract method"""
        raise NotImplementedError("Subclass must implement delete_wifi_interface()")

    @abstractmethod
    def set_vap_device(self, device: str, index: str, radio: str):
        """ Set VAP device abstract method"""
        raise NotImplementedError("Subclass must implement set_vap_device()")

    @abstractmethod
    def get_vap_device(self, device: str, index: str):
        """ Get VAP device abstract method"""
        raise NotImplementedError("Subclass must implement get_vap_device()")

    @abstractmethod
    def set_vap_name(self, device: str, index: str, name: str):
        """ Set VAP name abstract method"""
        raise NotImplementedError("Subclass must implement set_vap_name()")

    @abstractmethod
    def get_vap_name(self, device: str, index: str):
        """ Get VAP name abstract method"""
        raise NotImplementedError("Subclass must implement get_vap_name()")

    @abstractmethod
    def check_vap_mode(self, device: str, index: str, mode: str):
        """ Check VAP mode abstract method"""
        raise NotImplementedError("Subclass must implement check_vap_mode()")

    @abstractmethod
    def check_vap_ssid(self, device: str, index: str, ssid: str):
        """ Check VAP SSID abstract method"""
        raise NotImplementedError("Subclass must implement check_vap_ssid()")

    @abstractmethod
    def set_interface_state(self, device: str, index: str, state: str):
        """ Set interface state abstract method"""
        raise NotImplementedError("Subclass must implement set_interface_state()")

    @abstractmethod
    def get_interface_state(self, device: str, index: str):
        """ Get interface state abstract method"""
        raise NotImplementedError("Subclass must implement get_interface_state()")
