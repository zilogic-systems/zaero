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
Author: Zilogic Systems <code@zilogic.com>
"""
import serial
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger

class PDUError(Exception):
    """Represents an error in the PDU Controller."""


class PduController(DatabaseModule):
    """A library providing keywords for the ZUS-PDU Controller."""

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
        """Opens connection to the PDU Controller.

        The PDU Controller to connect to is specified by ``device``. This is
        generally the device name of the serial device corresponding to the USB
        PDU. An example of serial device name in Linux, is "/dev/ttyUSB0".

        *Example*

        | PDU Connect | /dev/ttyUSB0 |
        | PDU Connect | COM1         |
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
        """Closes connection to the PDU Controller."""
        zi_logger.print_context()
        try:
            self.PDU_interface.close()

        except (AttributeError, serial.serialutil.PortNotOpenError) as error:
            raise PDUError("No Device Connected") from error

    def _PDU(self, port: int, PDU_func=None) -> bytes:
        """Converts cmd to hex and writes to serial Device.

        - port - Switch ON the specified PDU.
        - PDU_func - Passing `toggle`/True/False. Defaults to ``True``.

        *Returns*

        _bytes_ - Returns bytes to Serial device.
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
        """Checks for the currently active ports.

        *Return:*
        List - Return active port list.
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
        """Check the PDU active status specified by ``port``.

        ``port`` must be a value in the range 1 to 8.

        *Return:*
        bool - Returns True if PDU is ON, else False

        *Example*

        | Check Port Active |  1 |
        | Check Port Active |  5 |
        """
        zi_logger.print_context()
        if port_num in self._check_ports():
            return True

        return False


    def check_all_active_ports(self,device) -> str:
        """Checks for all the active ports.

        *Return:*
        str - Return active ports in string format.
        """
        zi_logger.print_context()
        on_port_list = self._check_ports()
        ports = ", ".join(str(num) for num in on_port_list)

        return f"Currently on ports: {ports}"


    def check_port_on(self,device, port: int) -> None:
        """Checks specific port in a PDU is in ON state.

        ``port`` must be a value in the range 1 to 8.

        *Example*

        | Check Port ON |  1 |
        | Check Port ON |  5 |
        """
        zi_logger.print_context()
        if port in self._check_ports():
            return
        raise PDUError(f"{port} is in OFF state")


    def check_port_off(self,device, port: int) -> None:
        """Checks specific port in a PDU is in OFF state.

        ``port`` must be a value in the range 1 to 8.

        *Example*

        | Check Port OFF |  1 |
        | Check Port OFF |  5 |
        """
        zi_logger.print_context()
        if port not in self._check_ports():
            return
        raise PDUError(f'{port} is in ON state')


    def pdu_on(self, device, port: int) -> None:
        """Turn ON the PDU specified by ``port``.

        ``port`` must be a value in the range 1 to 8.

        *Example*

        | PDU ON |  1 |
        | PDU ON |  5 |
        """
        zi_logger.print_context()
        if self._PDU(port, "on"):
            return
        raise PDUError(f"Invalid command \n Unable to turn on port {port}")


    def pdu_off(self, device, port: int) -> None:
        """Turn OFF the PDU switch specified by ``port``.

        ``port`` must be a value in the range 1 to 8.

        *Example*

        | PDU OFF | 2 |
        | PDU OFF | 4 |
        """
        zi_logger.print_context()
        if self._PDU(port, "off"):
            return
        raise PDUError(f"Invalid command \n Unable to turn off port {port}")



    def pdu_switch_all(self,device) -> None:
        """Sets all PDUs to ON state."""
        zi_logger.print_context()
        if self._PDU("A", "on"):
            return
        raise PDUError("Unable to turn on all ports")


    def pdu_reset_all(self,device) -> None:
        """Sets all PDUs to OFF state."""
        zi_logger.print_context()
        if self._PDU("A", "off"):
            return
        raise PDUError("Unable to turn off all ports")

