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
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.platform_modules import PlatformModules
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger

class Radio(DatabaseModule,
            PlatformModules):

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        PlatformModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Radio __init__: END")

    @keyword("Load Wifi")
    def load_wifi(self,
                  device: str):
        """
        Load and re-initialize the wifi subsystem after modified
        the wireless configuration using *set* keywords

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        Example:
        | Load Wifi | ap |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.load_wifi(device)

    @keyword("Set Channel")
    def set_channel(self,
                    device: str,
                    index: str,
                    channel: int):
        """
        Set the operating channel for the given radio index.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``channel`` is the channel number has to be set in the ap
                      for the given radio

        Example:
        | Set Channel | ap | 2g_radio_index   | 11 |
        | Set Channel | ap | 5g_radio_index   | 48 |
        | Set Channel | ap | 6g_radio_index   | 1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_channel(device,
                                 index,
                                 channel)

    @keyword("Get Channel")
    def get_channel(self,
                    device: str,
                    index: str) -> int:
        """
        Get the currently configured channel of the given radio index.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the channel number for the given radio index

        Example:
        | ${ret}  |  Get Channel  |  ap  |  2g_radio_index  |
        | ${ret}  |  Get Channel  |  ap  |  5g_radio_index  |
        | ${ret}  |  Get Channel  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        channel = platform_obj.get_channel(device,
                                           index)
        return channel

    @keyword("Check Channel")
    def check_channel(self,
                      device: str,
                      index: str,
                      channel: int):
        """
        Check the currently configured channel of the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``channel`` is the channel number which has to be validated

        - ``Raise`` exception when the expected channel not matched
                    with configured channel

        Example:
        | Check Channel  |  ap  |  2g_radio_index  |  11   |
        | Check Channel  |  ap  |  5g_radio_index  |  40   |
        | Check Channel  |  ap  |  6g_radio_index  |  1    |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_channel(device,
                                   index,
                                   channel)

    @keyword("Set Bandwidth")
    def set_bandwidth(self,
                      device: str ,
                      index: str,
                      bandwidth: str,
                      no_scan: bool = False):
        """
        Set the channel bandwidth for the given radio index.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``bandwidth`` is the bandwidth has to be set in the ap
                        for the given radio

        Example:
        | Set Bandwidth | ap | 2g_radio_index | HT40   |
        | Set Bandwidth | ap | 5g_radio_index | VHT160 |
        | Set Bandwidth | ap | 6g_radio_index | EHT320 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_bandwidth(device,
                                   index,
                                   bandwidth,
                                   no_scan)

    @keyword("Get Bandwidth")
    def get_bandwidth(self,
                      device: str,
                      index: str) -> str:
        """
        Get the currently configured bandwidth of the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the bandwidth which has to be validated

        Example:
        | ${ret} | Get Bandwidth  |  ap  |  2g_radio_index  |
        | ${ret} | Get Bandwidth  |  ap  |  5g_radio_index  |
        | ${ret} | Get Bandwidth  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        bandwidth = platform_obj.get_bandwidth(device,
                                               index)
        return bandwidth

    @keyword("Check Bandwidth")
    def check_bandwidth(self,
                        device: str,
                        index: str,
                        bandwidth: int):
        """
        Check the currently configured bandwidth of the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``bandwidth`` is the number which has to be validated

        - ``Raise`` exception when the expected bandwidth not matched
                    with configured bandwidth

        Example:
        | Check Bandwidth  |  ap  |  2g_radio_index  |  20  |
        | Check Bandwidth  |  ap  |  5g_radio_index  |  80  |
        | Check Bandwidth  |  ap  |  6g_radio_index  |  160 |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_bandwidth(device,
                                   index,
                                   bandwidth)

    @keyword("Set Radio State")
    def set_radio_state(self,
                        device: str,
                        index: str,
                        state: int):
        """
        Enable or disable the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``state`` is the desired state of the radio
                    state == 1, Turns the radio ON
                    state == 0, Turns the radio OFF

        Example:
        | Set Radio State  |  ap  |  2g_radio_index  |  0  |
        | Set Radio State  |  ap  |  2g_radio_index  |  1  |
        | Set Radio State  |  ap  |  5g_radio_index  |  0  |
        | Set Radio State  |  ap  |  5g_radio_index  |  1  |
        | Set Radio State  |  ap  |  6g_radio_index  |  0  |
        | Set Radio State  |  ap  |  6g_radio_index  |  1  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_radio_state(device,
                                     index,
                                     state)

    @keyword("Get Radio State")
    def get_radio_state(self,
                        device: str,
                        index: str) -> bool:
        """
        Get the current state of the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` indicates the current state of the given radio index

        Example:
        | ${ret}  |  Get Radio State  |  ap  |  2g_radio_index  |
        | ${ret}  |  Get Radio State  |  ap  |  5g_radio_index  |
        | ${ret}  |  Get Radio State  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        state = platform_obj.get_radio_state(device,
                                             index)
        return state

    @keyword("Set Radio Standard")
    def set_radio_standard(self,
                           device: str,
                           index: str,
                           standard: str):
        """
        Set the wireless standard for the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``standard`` is the WiFi standard has to be set in the ap
                       for the given radio index

        Example:
        | Set Radio Standard  |  ap  |  2g_radio_index  |  11axg  |
        | Set Radio Standard  |  ap  |  5g_radio_index  |  11axa  |
        | Set Radio Standard  |  ap  |  6g_radio_index  |  11be   |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_radio_standard(device,
                                        index,
                                        standard)

    @keyword("Get Radio Standard")
    def get_radio_standard(self,
                           device: str,
                           index: str) -> str:
        """
        Get the wireless standard configured on the radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the WiFi standard which has to be validated

        Example:
        | ${ret} | Get Radio Standard  |  ap  |  2g_radio_index  |
        | ${ret} | Get Radio Standard  |  ap  |  5g_radio_index  |
        | ${ret} | Get Radio Standard  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        standard = platform_obj.get_radio_standard(device,
                                                   index)
        return standard

    @keyword("Set Txpower")
    def set_txpower(self,
                    device: str,
                    index: str,
                    txpower: int):
        """
        Set the transmission power (in dBm) for the radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``txpower`` is the transmit power has to be set in the ap for
                      the given radio index

        Example:
        | Set Txpower  |  ap  |  2g_radio_index    |  24  |
        | Set Txpower  |  ap  |  5g_radio_index    |  20  |
        | Set Txpower  |  ap  |  6g_radio_index    |  16  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_txpower(device,
                                  index,
                                  txpower)

    @keyword("Get Txpower")
    def get_txpower(self,
                    device: str,
                    index: str) -> int:
        """
        Get the current tx power configured on the radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the tx power which has to be validated

        Example:
        | ${ret}  | Get Txpower  |  ap  |  2g_radio_index  |
        | ${ret}  | Get Txpower  |  ap  |  5g_radio_index  |
        | ${ret}  | Get Txpower  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        txpower = platform_obj.get_txpower(device,
                                           index)
        return txpower

    @keyword("Check Txpower")
    def check_txpower(self,
                      device: str,
                      index: str,
                      txpower: int):
        """
        Check the currently configured tx power for the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``txpower`` is the tx power which has to be validated

        - ``Raise`` exception when the expected tx power not matched
                  with configured tx power

        Example:
        | Check Txpower  |  ap  |  2g_radio_index  |  24  |
        | Check Txpower  |  ap  |  5g_radio_index  |  20  |
        | Check Txpower  |  ap  |  6g_radio_index  |  16  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_txpower(device,
                                   index,
                                   txpower)

    @keyword("Set Noscan")
    def set_noscan(self,
                   device: str,
                   index: str,
                   state: int):
        """
        Set the wireless option noscan for radio 2G to set
        the bandwidth 40MHz

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``state`` is the desired state of the no scan
                    state == 1, Enable the no scan
                    state == 0, Disable the no scan

        Example:
        | Set Noscan  |  ap  |  2g_radio_index  |  1  |
        | Set Noscan  |  ap  |  2g_radio_index  |  0  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_noscan(device,
                                index,
                                state)

    @keyword("Set Prop Coext")
    def set_prop_coext(self,
                   device: str,
                   index: str):
        """
        Disable 20/40 MHz coexistence on the specified radio interface
        by running cfg80211tool disablecoext.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        Example:
        | Set Prop Coext  |  ap  |  2g_radio_index  |
        | Set Prop Coext  |  ap  |  5g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_prop_coext(device,
                                    index)


    @keyword("Set Prop Cfg")
    def set_prop_cfg(self,
                     device: str,
                     index: str):
        """
        Enable VHT (802.11ac) on a 2.4 GHz radio interface by running
        cfg80211tool vht_11ng, allowing 11ac clients on the 2G band.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        Example:
        | Set Prop Cfg  |  ap  |  2g_radio_index  |
        | Set Prop Cfg  |  ap  |  5g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_prop_cfg(device,
                                  index)

    @keyword("Get Noscan")
    def get_noscan(self,
                   device: str,
                   index: str) -> int:
        """
        Get the current noscan state configured on the radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the noscan state which has to be validated

        Example:
        | ${ret}  |  Get Noscan  |  ap  |  2g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        state = platform_obj.get_noscan(device,
                                        index)
        return state

    @keyword("Set Regulatory Domain")
    def set_regulatory_domain(self,
                              device: str,
                              reg_domain: str):
        """
        Set the regulatory domain (country code) for the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``reg_domain`` is the country code to be set on the ap
                         (e.g., US, GB, DE)

        Example:
        | Set Regulatory Domain  |  ap  |  US  |
        | Set Regulatory Domain  |  ap  |  GB  |
        | Set Regulatory Domain  |  ap  |  DE  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_regulatory_domain(device,
                                           reg_domain)

    @keyword("Set Country Regulatory Domain")
    def set_country_regulatory_domain(self,
                              device: str,
                              index: str,
                              reg_domain: str):
        """
        Set the country code on a specific radio via UCI
        (uci set wireless.<radio>.country=<reg_domain>).

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the radio index key (e.g., 2g_radio_index, 5g_radio_index)

        - ``reg_domain`` is the country code to be set (e.g., US, GB, DE)

        Example:
        | Set Country Regulatory Domain  |  ap  |  2g_radio_index  |  US  |
        | Set Country Regulatory Domain  |  ap  |  5g_radio_index  |  GB  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_country_regulatory_domain(device,index,reg_domain)

    @keyword("Get Regulatory Domain")
    def get_regulatory_domain(self,
                              device: str,
                              index: str) -> str:
        """
        Get the currently set regulatory domain for the radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the country code which has to validated

        Example:
        |  ${ret}  |  Get Regulatory Domain  |  ap  |  2g_radio_index  |
        |  ${ret}  |  Get Regulatory Domain  |  ap  |  5g_radio_index  |
        |  ${ret}  |  Get Regulatory Domain  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        reg_domain = platform_obj.get_regulatory_domain(device,
                                                        index)
        return reg_domain

    @keyword("Check Regulatory Domain")
    def check_regulatory_domain(self,
                                device: str,
                                index: str,
                                reg_domain: str):
        """
        Check the currently configured regulatory domain for the radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``reg_domain`` specifies the country code which has to be validated

        - ``Raise`` exception when the expected regulatory domain not matched
                    with configured regulatory domain

        Example:
        |  Check Regulatory Domain  |  ap  |  2g_radio_index  |  US  |
        |  Check Regulatory Domain  |  ap  |  5g_radio_index  |  GB  |
        |  Check Regulatory Domain  |  ap  |  6g_radio_index  |  DE  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.check_regulatory_domain(device,
                                             index,
                                             reg_domain)

    @keyword("Get Physical Interface Index")
    def get_physical_interface_index(self,
                                     device: str,
                                     index: str) -> int:
        """
        Get the physical interface index for the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the physical interface index which has to validated

        Example:
        |  ${ret} | Get Physical Interface Index  |  ap  |  2g_radio_index  |
        |  ${ret} | Get Physical Interface Index  |  ap  |  5g_radio_index  |
        |  ${ret} | Get Physical Interface Index  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        phy_iface_index = platform_obj.get_physical_interface_index(device,
                                                                    index)
        return phy_iface_index

    @keyword("Get Supported Channels Count")
    def get_supported_channels_count(self,
                                     device: str,
                                     index: str) -> int:
        """
        Get the supported channels count for the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the supported channels count which has to validated

        Example:
        |  ${ret} | Get Supported Channels Count  |  ap  |  2g_radio_index  |
        |  ${ret} | Get Supported Channels Count  |  ap  |  5g_radio_index  |
        |  ${ret} | Get Supported Channels Count  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        channels_count = platform_obj.get_supported_channels_count(device, index)
        return channels_count

    @keyword("Get Supported Channels List")
    def get_supported_channels_list(self,
                                    device: str,
                                    index: str) -> list:
        """
        Get the supported channels list for the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the supported channels list which has to validated

        Example:
        |  ${ret} | Get Supported Channels List  |  ap  |  2g_radio_index  |
        |  ${ret} | Get Supported Channels List  |  ap  |  5g_radio_index  |
        |  ${ret} | Get Supported Channels List  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        channels_list = platform_obj.get_supported_channels_list(device, index)
        return channels_list

    @keyword("Get Highest Supported Channel")
    def get_highest_supported_channel(self,
                                      device: str,
                                      index: str) -> int:
        """
        Get the highest supported channel for the given radio index

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the supported highest channel which has to validated

        Example:
        |  ${ret} | Get Highest Supported Channel  |  ap  |  2g_radio_index  |
        |  ${ret} | Get Highest Supported Channel  |  ap  |  5g_radio_index  |
        |  ${ret} | Get Highest Supported Channel  |  ap  |  6g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        channel = platform_obj.get_highest_supported_channel(device, index)
        return channel

    @keyword("Set Radio Type")
    def set_radio_type(self,
                 device: str,
                 index: str,
                 radio_type: str):
        """
        Set the wireless radio type for the given radio index.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``radio_type`` is the radio type to be set

        Example:
        | Set Radio Type  |  ap  |  2g_radio_index  |  qcawificfg80211  |
        | Set Radio Type  |  ap  |  5g_radio_index  |  qcawificfg80211  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        platform_obj.set_radio_type(device,
                              index,
                              radio_type)
    @keyword("Get Radio Type")
    def get_radio_type(self,
                 device: str,
                 index: str) -> str:
        """
        Get the wireless radio type configured for the given radio index.

        - ``device`` is the name given to the AP as mentioned
                     in the dut.yaml config file

        - ``index`` is the name given to the specific radio index
                    as mentioned in the dut.yaml config file

        - ``Returns`` the radio type for the given radio index

        Example:
        | ${ret}  |  Get Radio Type  |  ap  |  2g_radio_index  |
        | ${ret}  |  Get Radio Type  |  ap  |  5g_radio_index  |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        radio_type = platform_obj.get_radio_type(device, index)
        return radio_type
