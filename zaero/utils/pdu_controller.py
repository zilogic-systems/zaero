#
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
Driver for the ZUS USB PDU controller over a serial port.

Author: Zilogic Systems <code@zilogic.com>
"""
import serial
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger

class PDUError(Exception):
    """Represents an error in the PDU Controller."""


class PduController(DatabaseModule):
    """
    Driver for the ZUS USB PDU controller. Outlets 1 to 8 are switched by
    writing commands to the serial port.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
            zi_logger.print_context()
            self.PDU_interface = None
            DatabaseModule.__init__(self)
            self.__db_obj = self.get_database_module_object()
            zi_logger.log(f"==== db_obj : {self.__db_obj}")
            zi_logger.log("zaero.utila.PDUController.__init__() : END")

    def pdu_connect(self, device):
        """
        Open the serial port of the PDU at 115200 baud.

        - ``device`` is the serial port, e.g. ``/dev/ttyUSB0`` or ``COM1``.
          The PduControl keyword passes the ``serial_port`` from the config

        - ``Raises`` PDUError if the port could not be opened
        """
        zi_logger.print_context()
        try:
            self.PDU_interface = serial.Serial(
                device,
                baudrate=115200,
                timeout=2,
                write_timeout=2,
                parity=serial.PARITY_NONE,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
            )

        except (serial.SerialException, ValueError) as err:
            raise PDUError(f"Connection Failed {device}") from err

    
    def pdu_disconnect(self,device):
        """
        Close the serial port of the PDU.

        - ``device`` is not used

        - ``Raises`` PDUError if no PDU is connected
        """
        zi_logger.print_context()
        try:
            self.PDU_interface.close()

        except (AttributeError, serial.serialutil.PortNotOpenError) as error:
            raise PDUError("No Device Connected") from error

    def _PDU(self, port: int, PDU_func=None) -> bytes:
        """
        Write a command to the PDU and read the reply up to ``OK``.

        - ``port`` is the outlet number, or ``A`` for all outlets

        - ``PDU_func`` is ``on`` (``S<port>``), ``off`` (``C<port>``), ``read``
          (``R``), or anything else to toggle (``T<port>``)

        - ``Returns`` the reply as bytes
        """
        if PDU_func == "on":
            cmd = f"S{port}\r"
        elif PDU_func == "off":
            cmd = f"C{port}\r"
        elif PDU_func == "read":
            cmd = 'R'
        else: # Toggle ON/OFF
            cmd = f"T{port}"


        self.PDU_interface.write(cmd.encode())
        output = self.PDU_interface.read_until("OK".encode())
        return output

    def _check_ports(self) -> list:
        """
        Read the outlet states from the PDU.

        - ``Returns`` the list of outlet numbers that are on
        """
        res = self._PDU(port=0, PDU_func="read")
        char_to_remove = b"R\r\nOK"
        result_bytes = b""
        ports = []

        for char in res:
            byte_char = bytes([char])

            if byte_char not in char_to_remove:
                result_bytes += byte_char

        hex_value = result_bytes.decode("utf-8")

        decimal_value = int(hex_value, 16)

        for i in range(8):
            if decimal_value & (1 << (7 - i)):
                ports.append(i + 1)

        return ports


    def check_port_active(self, device, port_num: int) -> bool:
        """
        Check whether an outlet is on.

        - ``device`` is not used

        - ``port_num`` is the outlet number, 1 to 8

        - ``Returns`` True if the outlet is on, False otherwise
        """
        zi_logger.print_context()
        if port_num in self._check_ports():
            return True

        return False


    def check_all_active_ports(self,device) -> str:
        """
        Get the outlets that are on.

        - ``device`` is not used

        - ``Returns`` a string such as ``Currently on ports: 1, 3``
        """
        zi_logger.print_context()
        on_port_list = self._check_ports()
        ports = ", ".join(str(num) for num in on_port_list)

        return f"Currently on ports: {ports}"


    def check_port_on(self,device, port: int) -> None:
        """
        Check that an outlet is on.

        - ``device`` is not used

        - ``port`` is the outlet number, 1 to 8

        - ``Raises`` PDUError if the outlet is off
        """
        zi_logger.print_context()
        if port in self._check_ports():
            return
        raise PDUError(f"{port} is in OFF state")


    def check_port_off(self,device, port: int) -> None:
        """
        Check that an outlet is off.

        - ``device`` is not used

        - ``port`` is the outlet number, 1 to 8

        - ``Raises`` PDUError if the outlet is on
        """
        zi_logger.print_context()
        if port not in self._check_ports():
            return
        raise PDUError(f'{port} is in ON state')


    def pdu_on(self, device, port: int) -> None:
        """
        Turn on an outlet.

        - ``device`` is not used

        - ``port`` is the outlet number, 1 to 8

        - ``Raises`` PDUError if the PDU does not reply
        """
        zi_logger.print_context()
        if self._PDU(port, "on"):
            return
        raise PDUError(f"Invalid command \n Unable to turn on port {port}")


    def pdu_off(self, device, port: int) -> None:
        """
        Turn off an outlet.

        - ``device`` is not used

        - ``port`` is the outlet number, 1 to 8

        - ``Raises`` PDUError if the PDU does not reply
        """
        zi_logger.print_context()
        if self._PDU(port, "off"):
            return
        raise PDUError(f"Invalid command \n Unable to turn off port {port}")



    def pdu_switch_all(self,device) -> None:
        """
        Turn on all outlets.

        - ``device`` is not used

        - ``Raises`` PDUError if the PDU does not reply
        """
        zi_logger.print_context()
        if self._PDU("A", "on"):
            return
        raise PDUError("Unable to turn on all ports")


    def pdu_reset_all(self,device) -> None:
        """
        Turn off all outlets.

        - ``device`` is not used

        - ``Raises`` PDUError if the PDU does not reply
        """
        zi_logger.print_context()
        if self._PDU("A", "off"):
            return
        raise PDUError("Unable to turn off all ports")

