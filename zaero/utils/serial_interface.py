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
from robot.api.deco import keyword
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger


class SerialInterface(DatabaseModule):
    """
    A library to establish serial console connections into devices
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

        ``serial_port`` is the serial device, e.g. /dev/ttyUSB0
        and ``alias`` is the reference name for this connection
        and ``baudrate`` is the baud rate of the serial port
        and ``timeout`` is the read timeout in seconds
        and ``write_timeout`` is the write timeout in seconds

        ``raise`` RuntimeError if the given alias is already registered
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
        Connect to the given device over its serial port, using the
        ``serial_port`` and ``serial_baudrate`` from the database.

        ``device`` is the reference name of the device

        ``returns`` True if connected, else False
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
        Switch the SSH connection into the specifice device

        ``alias`` the reference name assigned to the ssh client object
        of the remote device

        ``raise`` a runtime error if the reference alias name is not
        present in the database dictionary

        Example:
        | Switch To Connection | ap                        |
        | Switch To Connection | ap_lan_client_01          |
        | Switch To Connection | ap_wlan_client_02         |
        | Switch To Connection | repeate_01
        | Switch To Connection | repeater_01_lan_client_01 |
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
        Write the command into the serial console and read the output
        until the shell prompt, stripping the echoed command and the prompt.
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
                        blocking_call:bool =True,
                        prompt: str = "#"):
        """
        Execute the given command in the device over the serial console

        ``device`` is the reference name of the device
        and ``command`` is the command to be executed in the device
        and ``return_stdout`` is to return the stdout of the command executed
        and ``return_stderr`` is to return the stderr of the command executed;
        the serial console merges stderr into stdout, so it is always empty
        and ``return_rc`` is to return the return code of the command executed
        and ``blocking_call`` is to select whether to wait for the command output
        and ``prompt`` is the shell prompt marking the end of the output

        ``returns`` the combination of stdout, std_err, and return code based on
        the arguments provided

        ``raise`` a runtime error if could not execute the command in the device
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
        Close the serial connection of the given device.

        ``device`` is the reference name of the device

        ``raise`` RuntimeError if the device is not connected or could not be closed
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
        """
        Close all the established serial connections.
        """

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




