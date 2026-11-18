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
Abstract base class for WiFi interface (VAP) configuration methods.

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod


class BaseFeatureInterface(ABC):
    """
    Abstract methods a platform plugin implements for WiFi interface (VAP) configuration.
    Implemented by external platform plugins for access points.
    """

    @abstractmethod
    def set_ssid(self, device: str, index: str, ssid: str):
        """
        Set the SSID of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``ssid`` is the SSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_ssid()")

    @abstractmethod
    def set_interface_from_database(self, device: str, index: str):
        """
        Configure the WiFi interface with the values stored in the database for the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_interface_from_database()")

    @abstractmethod
    def get_interface(self, device: str, index: str):
        """
        Get the name of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the interface name

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_interface()")

    @abstractmethod
    def check_interface(self, device: str, index: str):
        """
        Check that the WiFi interface exists.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_interface()")

    @abstractmethod
    def get_ssid(self, device: str, index: str):
        """
        Get the SSID of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the SSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_ssid()")

    @abstractmethod
    def check_ssid(self, device: str, index: str, ssid: str):
        """
        Check that the WiFi interface uses the given SSID.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``ssid`` is the SSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_ssid()")

    @abstractmethod
    def set_encryption(self, device: str, index: str, encryption: str):
        """
        Set the encryption of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``encryption`` is the encryption mode

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_encryption()")

    @abstractmethod
    def get_encryption(self, device: str, index: str):
        """
        Get the encryption of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the encryption mode

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_encryption()")

    @abstractmethod
    def set_password(self, device: str, index: str, password: str):
        """
        Set the password of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``password`` is the WiFi password, or None for an open network

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_password()")

    @abstractmethod
    def get_password(self, device: str, index: str):
        """
        Get the password of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the password

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_password()")

    @abstractmethod
    def set_sae_parameters(self, device: str, index: str, password: str):
        """
        Set the WPA3 SAE parameters of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``password`` is the WiFi password, or None for an open network

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_sae_parameters()")

    @abstractmethod
    def check_brctl_show(self, device: str, bridge: str, interface: str):
        """
        Check with ``brctl show`` that the interface is part of the bridge.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``bridge`` is the bridge interface name

        - ``interface`` is the network interface name

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_brctl_show()")

    @abstractmethod
    def get_dut_bridge_ipv4(self, device: str, bridge: str):
        """
        Get the IPv4 address of a bridge on the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``bridge`` is the bridge interface name

        - ``Returns`` the IPv4 address

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_dut_bridge_ipv4()")

    @abstractmethod
    def get_dut_wan_ipv4(self, device: str, interface: str):
        """
        Get the IPv4 address of the WAN interface of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``interface`` is the network interface name

        - ``Returns`` the IPv4 address

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_dut_wan_ipv4()")

    @abstractmethod
    def set_wifi_iface_device(self, device: str, index: str, radio: str):
        """
        Set the radio the WiFi interface belongs to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``radio`` is the radio the interface belongs to

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_wifi_iface_device()")

    @abstractmethod
    def get_wifi_iface_device(self, device: str, index: str):
        """
        Get the radio the WiFi interface belongs to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the radio

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_wifi_iface_device()")

    @abstractmethod
    def set_wifi_iface_network(self, device: str, index: str, network: str):
        """
        Set the network the WiFi interface is attached to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``network`` is the network the interface is attached to

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_wifi_iface_network()")

    @abstractmethod
    def get_wifi_iface_network(self, device: str, index: str):
        """
        Get the network the WiFi interface is attached to.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the network

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_wifi_iface_network()")

    @abstractmethod
    def set_wifi_iface_mode(self, device: str, index: str, mode: str):
        """
        Set the mode of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``mode`` is the interface mode, e.g. ``ap`` or ``sta``

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_wifi_iface_mode()")

    @abstractmethod
    def get_wifi_iface_mode(self, device: str, index: str):
        """
        Get the mode of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the mode

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_wifi_iface_mode()")

    @abstractmethod
    def check_mode(self, device: str, index: str, mode: str):
        """
        Check that the WiFi interface is in the given mode.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``mode`` is the interface mode, e.g. ``ap`` or ``sta``

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_mode()")

    @abstractmethod
    def set_wifi_iface_isolate(self, device: str, index: str, isolate: str):
        """
        Set client isolation on the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``isolate`` is the client isolation setting

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_wifi_iface_isolate()")

    @abstractmethod
    def get_wifi_iface_isolate(self, device: str, index: str):
        """
        Get the client isolation setting of the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the isolation setting

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_wifi_iface_isolate()")

    @abstractmethod
    def add_wifi_interface(self, device: str, index: str):
        """
        Add a WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement add_wifi_interface()")

    @abstractmethod
    def delete_wifi_interface(self, device: str, index: str):
        """
        Delete a WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement delete_wifi_interface()")

    @abstractmethod
    def set_vap_device(self, device: str, index: str, radio: str):
        """
        Set the radio of the VAP.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``radio`` is the radio the interface belongs to

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_vap_device()")

    @abstractmethod
    def get_vap_device(self, device: str, index: str):
        """
        Get the radio of the VAP.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the radio

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_vap_device()")

    @abstractmethod
    def set_vap_name(self, device: str, index: str, name: str):
        """
        Set the name of the VAP.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``name`` is the VAP name

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_vap_name()")

    @abstractmethod
    def get_vap_name(self, device: str, index: str):
        """
        Get the name of the VAP.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the VAP name

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_vap_name()")

    @abstractmethod
    def check_vap_mode(self, device: str, index: str, mode: str):
        """
        Check that the VAP is in the given mode.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``mode`` is the interface mode, e.g. ``ap`` or ``sta``

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_vap_mode()")

    @abstractmethod
    def check_vap_ssid(self, device: str, index: str, ssid: str):
        """
        Check that the VAP uses the given SSID.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``ssid`` is the SSID

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_vap_ssid()")

    @abstractmethod
    def set_interface_state(self, device: str, index: str, state: str):
        """
        Enable or disable the WiFi interface.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``state`` is the desired state

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_interface_state()")

    @abstractmethod
    def get_interface_state(self, device: str, index: str):
        """
        Get whether the WiFi interface is enabled.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the interface state

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_interface_state()")
