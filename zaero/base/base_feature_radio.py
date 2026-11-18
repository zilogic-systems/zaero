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
Abstract base class for WiFi radio configuration methods.

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod


class BaseFeatureRadio(ABC):
    """
    Abstract methods a platform plugin implements for WiFi radio configuration.
    Implemented by external platform plugins for access points.
    """

    @abstractmethod
    def load_wifi(self, device: str):
        """
        Load the WiFi configuration of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement load_wifi()")

    @abstractmethod
    def set_channel(self, device: str, index: str, channel: str):
        """
        Set the channel of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``channel`` is the channel number

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_channel()")

    @abstractmethod
    def get_channel(self, device: str, index: str):
        """
        Get the channel of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the channel

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_channel()")

    @abstractmethod
    def check_channel(self, device: str, index: str, channel: str):
        """
        Check that the radio is on the given channel.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``channel`` is the channel number

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_channel()")

    @abstractmethod
    def check_regulatory_domain(self, device: str, index: str, reg_domain: str):
        """
        Check that the radio uses the given regulatory domain.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``reg_domain`` is the regulatory domain

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_regulatory_domain()")

    @abstractmethod
    def get_physical_interface_index(self, device: str, index: str):
        """
        Get the physical interface index of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the physical interface index

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_physical_interface_index()")

    @abstractmethod
    def get_supported_channels_count(self, device: str, index: str):
        """
        Get the number of channels the radio supports.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the number of channels

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_supported_channels_count()")

    @abstractmethod
    def get_supported_channels_list(self, device: str, index: str):
        """
        Get the channels the radio supports.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the list of channels

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_supported_channels_list()")

    @abstractmethod
    def get_highest_supported_channel(self, device: str, index: str):
        """
        Get the highest channel the radio supports.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the channel

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_highest_supported_channel()")

    @abstractmethod
    def set_bandwidth(self, device: str, index: str, bandwidth: str):
        """
        Set the channel width of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``bandwidth`` is the channel width

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_bandwidth()")

    @abstractmethod
    def get_bandwidth(self, device: str, index: str):
        """
        Get the channel width of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the channel width

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_bandwidth()")

    @abstractmethod
    def check_bandwidth(self, device: str, index: str, bandwidth: str):
        """
        Check that the radio uses the given channel width.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``bandwidth`` is the channel width

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_bandwidth()")

    @abstractmethod
    def set_radio_state(self, device: str, index: str, state: str):
        """
        Enable or disable the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``state`` is the desired state

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_radio_state()")

    @abstractmethod
    def get_radio_state(self, device: str, index: str):
        """
        Get whether the radio is enabled.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the radio state

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_radio_state()")

    @abstractmethod
    def set_radio_standard(self, device: str, index: str, standard: str):
        """
        Set the WiFi standard of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``standard`` is the WiFi standard, e.g. ``ax``

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_radio_standard()")

    @abstractmethod
    def get_radio_standard(self, device: str, index: str):
        """
        Get the WiFi standard of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the WiFi standard

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_radio_standard()")

    @abstractmethod
    def set_txpower(self, device: str, index: str, txpower: str):
        """
        Set the transmit power of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``txpower`` is the transmit power

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_txpower()")

    @abstractmethod
    def get_txpower(self, device: str, index: str):
        """
        Get the transmit power of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the transmit power

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_txpower()")

    @abstractmethod
    def check_txpower(self, device: str, index: str, txpower: str):
        """
        Check that the radio uses the given transmit power.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``txpower`` is the transmit power

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement check_txpower()")

    @abstractmethod
    def set_noscan(self, device: str, index: str, noscan: str):
        """
        Set the noscan option of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``noscan`` is the noscan setting

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_noscan()")

    @abstractmethod
    def get_noscan(self, device: str, index: str):
        """
        Get the noscan option of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the noscan setting

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_noscan()")

    @abstractmethod
    def set_prop_coext(self, device: str, index: str, coext: str):
        """
        Set the vendor specific coexistence option of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``coext`` is the coexistence setting

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_prop_coext()")

    @abstractmethod
    def set_prop_cfg(self, device: str, index: str, cfg: str):
        """
        Set a vendor specific configuration option of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``cfg`` is the vendor specific configuration value

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_prop_cfg()")

    @abstractmethod
    def set_regulatory_domain(self, device: str, index: str, reg_domain: str):
        """
        Set the regulatory domain of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``reg_domain`` is the regulatory domain

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_regulatory_domain()")

    @abstractmethod
    def set_country_regulatory_domain(self, device: str, index: str, country: str):
        """
        Set the regulatory domain of the radio from a country code.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``country`` is the country code

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_country_regulatory_domain()")

    @abstractmethod
    def get_regulatory_domain(self, device: str, index: str):
        """
        Get the regulatory domain of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the regulatory domain

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_regulatory_domain()")

    @abstractmethod
    def set_radio_type(self, device: str, index: str, radio_type: str):
        """
        Set the type of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``radio_type`` is the radio type

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement set_radio_type()")

    @abstractmethod
    def get_radio_type(self, device: str, index: str):
        """
        Get the type of the radio.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``index`` is the radio or interface index, as used by the platform plugin

        - ``Returns`` the radio type

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_radio_type()")
