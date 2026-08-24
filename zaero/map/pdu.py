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
Author: Zilogic Systems <code@zilogic.com>
"""
# from zaero.bridge.connection_modules import ConnectionModules
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger
from zaero.bridge.utils_modules import UtilsModules
from robot.api.deco import keyword


class PduControl(DatabaseModule,UtilsModules):

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        UtilsModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log("PDUControl __init__ : END")

    @keyword("Pdu Connect")
    def pdu_connect(self, device):
        zi_logger.print_context()
        serial_port = self.db_obj.read_from_database(device, "serial_port")
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_connect(serial_port)
        return utils_obj

    @keyword("Pdu ON")
    def pdu_on(self, device, port: int) -> None:
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_on(device,port)
        return utils_obj

    @keyword("Check Port ON")
    def check_port_on(self,device, port: int) -> None:
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.check_port_on(device,port)
        return utils_obj

    @keyword("Pdu OFF")
    def pdu_off(self, device, port: int) -> None:
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_off(device,port)
        return utils_obj

    @keyword("Check Port Off")
    def check_port_off(self,device, port: int) -> None:
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.check_port_off(device,port)
        return utils_obj

    @keyword("Pdu Switch All")
    def pdu_switch_all(self,device) -> None:

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_switch_all(device)
        return utils_obj

    @keyword("Pdu Reset All")
    def pdu_reset_all(self,device) -> None:

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_reset_all(device)
        return utils_obj

    @keyword("Check Port Active")
    def check_port_active(self, device, port_num: int) -> bool:

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.check_port_active(device,port_num)
        return utils_obj

    @keyword("Pdu Disconnect")
    def pdu_disconnect(self,device):

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_disconnect(device)
        return utils_obj

