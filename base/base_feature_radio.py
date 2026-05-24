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
This module handles radio abstract methods

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod


class BaseFeatureRadio(ABC):
    """ This module provides abstract class for the APIs in radio"""

    @abstractmethod
    def load_wifi(self, device: str):
        """ Load wifi abstract method"""
        raise NotImplementedError("Subclass must implement load_wifi()")

    @abstractmethod
    def set_channel(self, device: str, index: str, channel: str):
        """ Set channel abstract method"""
        raise NotImplementedError("Subclass must implement set_channel()")

    @abstractmethod
    def get_channel(self, device: str, index: str):
        """ Get channel abstract method"""
        raise NotImplementedError("Subclass must implement get_channel()")

    @abstractmethod
    def check_channel(self, device: str, index: str, channel: str):
        """ Check channel abstract method"""
        raise NotImplementedError("Subclass must implement check_channel()")

    @abstractmethod
    def check_regulatory_domain(self, device: str, index: str, reg_domain: str):
        """ Check regulatory domain abstract method"""
        raise NotImplementedError("Subclass must implement check_regulatory_domain()")

    @abstractmethod
    def get_physical_interface_index(self, device: str, index: str):
        """ Get physical interface index abstract method"""
        raise NotImplementedError("Subclass must implement get_physical_interface_index()")

    @abstractmethod
    def get_supported_channels_count(self, device: str, index: str):
        """ Get supported channels count abstract method"""
        raise NotImplementedError("Subclass must implement get_supported_channels_count()")

    @abstractmethod
    def get_supported_channels_list(self, device: str, index: str):
        """ Get supported channels list abstract method"""
        raise NotImplementedError("Subclass must implement get_supported_channels_list()")

    @abstractmethod
    def get_highest_supported_channel(self, device: str, index: str):
        """ Get highest supported channel abstract method"""
        raise NotImplementedError("Subclass must implement get_highest_supported_channel()")

    @abstractmethod
    def set_bandwidth(self, device: str, index: str, bandwidth: str):
        """ Set bandwidth abstract method"""
        raise NotImplementedError("Subclass must implement set_bandwidth()")

    @abstractmethod
    def get_bandwidth(self, device: str, index: str):
        """ Get bandwidth abstract method"""
        raise NotImplementedError("Subclass must implement get_bandwidth()")

    @abstractmethod
    def check_bandwidth(self, device: str, index: str, bandwidth: str):
        """ Check bandwidth abstract method"""
        raise NotImplementedError("Subclass must implement check_bandwidth()")

    @abstractmethod
    def set_radio_state(self, device: str, index: str, state: str):
        """ Set radio state abstract method"""
        raise NotImplementedError("Subclass must implement set_radio_state()")

    @abstractmethod
    def get_radio_state(self, device: str, index: str):
        """ Get radio state abstract method"""
        raise NotImplementedError("Subclass must implement get_radio_state()")

    @abstractmethod
    def set_radio_standard(self, device: str, index: str, standard: str):
        """ Set radio standard abstract method"""
        raise NotImplementedError("Subclass must implement set_radio_standard()")

    @abstractmethod
    def get_radio_standard(self, device: str, index: str):
        """ Get radio standard abstract method"""
        raise NotImplementedError("Subclass must implement get_radio_standard()")

    @abstractmethod
    def set_txpower(self, device: str, index: str, txpower: str):
        """ Set transmit power abstract method"""
        raise NotImplementedError("Subclass must implement set_txpower()")

    @abstractmethod
    def get_txpower(self, device: str, index: str):
        """ Get transmit power abstract method"""
        raise NotImplementedError("Subclass must implement get_txpower()")

    @abstractmethod
    def check_txpower(self, device: str, index: str, txpower: str):
        """ Check transmit power abstract method"""
        raise NotImplementedError("Subclass must implement check_txpower()")

    @abstractmethod
    def set_noscan(self, device: str, index: str, noscan: str):
        """ Set noscan abstract method"""
        raise NotImplementedError("Subclass must implement set_noscan()")

    @abstractmethod
    def get_noscan(self, device: str, index: str):
        """ Get noscan abstract method"""
        raise NotImplementedError("Subclass must implement get_noscan()")

    @abstractmethod
    def set_prop_coext(self, device: str, index: str, coext: str):
        """ Set coexistence property abstract method"""
        raise NotImplementedError("Subclass must implement set_prop_coext()")

    @abstractmethod
    def set_prop_cfg(self, device: str, index: str, cfg: str):
        """ Set cfg80211 property abstract method"""
        raise NotImplementedError("Subclass must implement set_prop_cfg()")

    @abstractmethod
    def set_regulatory_domain(self, device: str, index: str, reg_domain: str):
        """ Set regulatory domain abstract method"""
        raise NotImplementedError("Subclass must implement set_regulatory_domain()")

    @abstractmethod
    def set_country_regulatory_domain(self, device: str, index: str, country: str):
        """ Set country regulatory domain abstract method"""
        raise NotImplementedError("Subclass must implement set_country_regulatory_domain()")

    @abstractmethod
    def get_regulatory_domain(self, device: str, index: str):
        """ Get regulatory domain abstract method"""
        raise NotImplementedError("Subclass must implement get_regulatory_domain()")

    @abstractmethod
    def set_radio_type(self, device: str, index: str, radio_type: str):
        """ Set radio type abstract method"""
        raise NotImplementedError("Subclass must implement set_radio_type()")

    @abstractmethod
    def get_radio_type(self, device: str, index: str):
        """ Get radio type abstract method"""
        raise NotImplementedError("Subclass must implement get_radio_type()")
