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
Robot Framework keywords to control a USB PDU (power distribution unit).

Author: Zilogic Systems <code@zilogic.com>
"""
# from zaero.bridge.connection_modules import ConnectionModules
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger
from zaero.bridge.utils_modules import UtilsModules
from robot.api.deco import keyword


class PduControl(DatabaseModule,UtilsModules):
    """
    Keywords to switch the power outlets of a USB PDU over its serial port.
    The serial port is read from the ``pdu`` entry of the config, which
    also maps each device to its outlet number.
    """

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
        """
        Open the serial connection to the PDU.

        - ``device`` is the PDU name in the config, e.g. ``pdu``. Its
          ``serial_port`` is used

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if the serial port could not be opened

        Example:
        | Pdu Connect | pdu |
        """
        zi_logger.print_context()
        serial_port = self.db_obj.read_from_database(device, "serial_port")
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_connect(serial_port)
        return utils_obj

    @keyword("Pdu ON")
    def pdu_on(self, device, port: int) -> None:
        """
        Turn on a PDU outlet.

        - ``device`` is the PDU name in the config

        - ``port`` is the outlet number, 1 to 8

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if the PDU does not answer

        Example:
        | Pdu ON | pdu | 2 |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_on(device,port)
        return utils_obj

    @keyword("Check Port ON")
    def check_port_on(self,device, port: int) -> None:
        """
        Check that a PDU outlet is on.

        - ``device`` is the PDU name in the config

        - ``port`` is the outlet number, 1 to 8

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if the outlet is off

        Example:
        | Check Port ON | pdu | 2 |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.check_port_on(device,port)
        return utils_obj

    @keyword("Pdu OFF")
    def pdu_off(self, device, port: int) -> None:
        """
        Turn off a PDU outlet.

        - ``device`` is the PDU name in the config

        - ``port`` is the outlet number, 1 to 8

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if the PDU does not answer

        Example:
        | Pdu OFF | pdu | 2 |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_off(device,port)
        return utils_obj

    @keyword("Check Port Off")
    def check_port_off(self,device, port: int) -> None:
        """
        Check that a PDU outlet is off.

        - ``device`` is the PDU name in the config

        - ``port`` is the outlet number, 1 to 8

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if the outlet is on

        Example:
        | Check Port Off | pdu | 2 |
        """
        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.check_port_off(device,port)
        return utils_obj

    @keyword("Pdu Switch All")
    def pdu_switch_all(self,device) -> None:
        """
        Turn on all PDU outlets.

        - ``device`` is the PDU name in the config

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if the PDU does not answer

        Example:
        | Pdu Switch All | pdu |
        """

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_switch_all(device)
        return utils_obj

    @keyword("Pdu Reset All")
    def pdu_reset_all(self,device) -> None:
        """
        Turn off all PDU outlets.

        - ``device`` is the PDU name in the config

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if the PDU does not answer

        Example:
        | Pdu Reset All | pdu |
        """

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_reset_all(device)
        return utils_obj

    @keyword("Check Port Active")
    def check_port_active(self, device, port_num: int) -> bool:
        """
        Check whether a PDU outlet is on.

        Note: the keyword returns the PduController object, not the result of
        the check.

        - ``device`` is the PDU name in the config

        - ``port_num`` is the outlet number, 1 to 8

        - ``Returns`` the PduController object

        Example:
        | Check Port Active | pdu | 2 |
        """

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.check_port_active(device,port_num)
        return utils_obj

    @keyword("Pdu Disconnect")
    def pdu_disconnect(self,device):
        """
        Close the serial connection to the PDU.

        - ``device`` is the PDU name in the config

        - ``Returns`` the PduController object

        - ``Raises`` PDUError if no PDU is connected

        Example:
        | Pdu Disconnect | pdu |
        """

        zi_logger.print_context()
        utils_obj = self.get_utils_module_object('pdu')
        utils_obj.pdu_disconnect(device)
        return utils_obj

