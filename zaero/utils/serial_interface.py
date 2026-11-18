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
Serial console connection module based on pyserial.

Author: Zilogic Systems <code@zilogic.com>
"""
import serial
from robot.api.deco import keyword
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger


class SerialInterface(DatabaseModule):
    """
    Connection module for devices reached over a serial console. Used for
    devices with ``connection: 'serial'``.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'global'

    __objects = {}
    __alias = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        zi_logger.print_context()
        if cls.__instance is None:
            zi_logger.log("SerialInterface Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        self.__db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.__db_obj}")
        zi_logger.log("utila.serial_interface.__init__() : END")


    def __open_connection(self,
                            serial_port: str,
                            alias: str = None,
                            baudrate: int = 115200,
                            timeout: int = 2,
                            write_timeout: int =2):
        """
        Open the serial port of a device and register it under an alias.

        - ``serial_port`` is the serial device, e.g. ``/dev/ttyUSB0``

        - ``alias`` is the connection name, normally the device name

        - ``baudrate`` is the baud rate

        - ``timeout`` is the read timeout in seconds

        - ``write_timeout`` is the write timeout in seconds

        - ``Raises`` RuntimeError if the alias is already registered
        """
        zi_logger.print_context()
        if alias is not None and alias in SerialInterface.__objects:
            raise RuntimeError(f"ERROR : Given alias name {alias} is already created")

        zi_logger.log(f"========= ALIAS IS : {alias}")
        SerialInterface.__objects[alias] = {}
        SerialInterface.__objects[alias]["serial_port"] = serial_port
        SerialInterface.__objects[alias]["baudrate"] = baudrate
        SerialInterface.__objects[alias]["timeout"] = timeout

        SerialInterface.__objects[alias]["serial"] = serial.Serial(
                                                                port=serial_port,
                                                                baudrate=baudrate,
                                                                timeout=timeout,
                                                                write_timeout=write_timeout,
                                                                parity=serial.PARITY_NONE,
                                                                bytesize=serial.EIGHTBITS,
                                                                stopbits=serial.STOPBITS_ONE)
        SerialInterface.__alias = alias

        zi_logger.log(f"========= ALIAS List : {SerialInterface.__objects.keys()}")


    def connect_with_device(self,
                             device: str):
        """
        Open the serial connection of the device with ``serial_port`` and
        ``serial_baudrate`` from the config.

        - ``device`` is the device name

        - ``Returns`` True if connected, False otherwise
        """

        zi_logger.print_context()

        try:
            serial_port = self.__db_obj.read_from_database(device,"serial_port")
            baudrate = self.__db_obj.read_from_database(device,"serial_baudrate")
            self.__open_connection(serial_port=serial_port,alias=device,baudrate=baudrate)
            zi_logger.log(f"Connected with device : {device}")
            return True
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"Could not login into the device : {device}", "error")
            return False
    
    def switch_connection(self,
                          alias: str):
        """
        Make the given connection the current one.

        - ``alias`` is the device name

        - ``Raises`` RuntimeError if the device is not connected
        """
        zi_logger.print_context()
        if alias not in SerialInterface.__objects:
            raise RuntimeError(f"Given alias - {alias} is not present")        
        zi_logger.log(f"switch_connection : device - {alias}")
        SerialInterface.__alias = alias

    def __run_command(self,
                      ser,
                      command: str,
                      prompt: str) -> str:
        """
        Write a command to the serial console and read until the prompt.

        - ``ser`` is the open serial port

        - ``command`` is the command to run

        - ``prompt`` is the shell prompt that ends the output

        - ``Returns`` the output without the echoed command and the prompt
        """
        ser.reset_input_buffer()
        ser.write(f"{command}\n".encode())
        output = ser.read_until(prompt.encode())
        output = output.decode("utf-8",errors="ignore")
        lines = output.strip().splitlines()
        lines = lines[1:-1]
        return "\n".join(lines).strip()

    def execute_command(self, # pylint: disable=R0913
                        device: str,
                        command: str,
                        return_stdout: bool =True,
                        return_stderr: bool =False,
                        return_rc:bool =False,
                        timeout: int = 10,
                        blocking_call:bool =True):
                        #prompt: str = "#"):
        """
        Run a command on the device over the serial console. The prompt that
        ends the output is read from the ``prompt`` field of the device config.

        - ``device`` is the device name

        - ``command`` is the command to run

        - ``return_stdout`` if True, return the output

        - ``return_stderr`` if True, return the stderr. The console merges
          stderr into the output, so this is always an empty string

        - ``return_rc`` if True, return the exit code, read with ``echo $?``

        - ``timeout`` is not used; the port read timeout applies

        - ``blocking_call`` if False, write the command and return None without
          reading the output

        - ``Returns`` the selected values in the order stdout, stderr, exit code.
          A single value is returned as is, several as a tuple, none as None

        - ``Raises`` RuntimeError if the device is not connected or the command
          could not be run
        """
        zi_logger.print_context()
        if device not in SerialInterface.__objects:
            raise RuntimeError(f"Device {device} is not connected")
        try:
            ser = SerialInterface.__objects[device]["serial"]
            zi_logger.log(f"COMMAND : {command}")
            if not blocking_call:
                ser.reset_input_buffer()
                ser.write(f"{command}\n".encode())
                return None

            prompt = self.__db_obj.read_from_database(device,"prompt")
            output = self.__run_command(ser, command, prompt)
            error = ""
            return_code = None
            if return_rc:
                return_code = int(self.__run_command(ser, "echo $?", prompt))

            out = []
            if return_stdout:
                out.append(output)
            if return_stderr:
                out.append(error)
            if return_rc:
                out.append(return_code)
            if not out:
                out = None
            elif len(out) == 1:
                out = out[0]
            else:
                out = tuple(out)
            zi_logger.log(f"OUTPUT : {out}")
            return out
        except Exception as err:
            zi_logger.log(f"Could not execute the command - {command}", status="ERROR")
            raise RuntimeError(err) from err

    def close_connection(self,
                         device: str):
        """
        Close the serial connection of the device.

        - ``device`` is the device name

        - ``Raises`` RuntimeError if the device is not connected or the port
          could not be closed
        """

        zi_logger.print_context()
        if device not in SerialInterface.__objects:
            raise RuntimeError(f"Device {device} is not connected")
        try:
            SerialInterface.__objects[device]["serial"].close()
            del SerialInterface.__objects[device]
            zi_logger.log(f"Closed connection : {device}")
        except Exception as err:
            zi_logger.log(f"ERROR: {err}", "error")
            raise RuntimeError(err) from err

    def close_all_connections(self):
        """Close all serial connections and forget them."""

        zi_logger.print_context()
        aliases = list(SerialInterface.__objects.keys())
        if len(aliases) >= 1:
            for alias in aliases:
                try:
                    SerialInterface.__objects[alias]["serial"].close()
                except Exception as err: # pylint: disable=broad-except
                        zi_logger.log(f"ERROR: {err}", "error")
                        zi_logger.log(f"Could not close the serial connection for the alias : {alias}")
            SerialInterface.__objects = {}
            zi_logger.log("All serial connections closed")




