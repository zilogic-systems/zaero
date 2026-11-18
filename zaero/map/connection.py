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
Robot Framework keywords to connect to devices and run commands on them.

Author: Zilogic Systems <code@zilogic.com>
"""
# Third-party Libraries
from robot.api.deco import keyword

# Local Libraries
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger

class Connection(DatabaseModule,
                 ConnectionModules):
    """
    Keywords to connect to devices and run commands over SSH, ADB or serial.
    Each keyword reads the ``connection`` of the device and calls the
    matching connection module.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Connection __init__ : END")

    @keyword("Connect With Device")
    def connect_with_device(self,
                            device: str):
        """
        Connect to the device using its ``connection`` type.

        Does nothing if ``device_present`` of the device is False.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` True if connected, False if the connection failed (SSH),
          or None if the device is not present

        Example:
        | Connect With Device | controller |
        | Connect With Device | extender1  |
        """
        zi_logger.print_context()
        state = self.db_obj.read_from_database(device, 'device_present')
        zi_logger.log(f"State: {state}")

        if state:
            connection = self.db_obj.read_device_connection(device)
            zi_logger.log(f"Connection : {connection}")
            connection_obj = self.get_connection_module_object(connection)
            zi_logger.log(f"connection_obj: {connection_obj}")
            status = connection_obj.connect_with_device(device)
            return status

    @keyword("Is Device Alive")
    def is_device_alive(self,
                        device: str):
        """
        Check whether the connection to the device is still active.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` True if the device answers, False otherwise

        - ``Raises`` RuntimeError if the device was never connected

        Example:
        | ${alive} | Is Device Alive | controller |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        return connection_obj.is_device_alive(device)

    @keyword("Execute Command")
    def execute_command(self,
                        device,
                        command: str,
                        return_stdout: bool =True,
                        return_stderr: bool =False,
                        return_rc:bool =False,
                        timeout: int = 30,
                        blocking_call:bool =True):
        """
        Run a shell command on the device and return the requested output.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``command`` is the shell command to run

        - ``return_stdout`` if True, return the stdout (default: True)

        - ``return_stderr`` if True, return the stderr (default: False).
          Always empty for serial connections

        - ``return_rc`` if True, return the exit code (default: False)

        - ``timeout`` is the command timeout in seconds (default: 30)

        - ``blocking_call`` if True, wait for the command to finish (default:
          True). If False, the command is started in the background and None
          is returned

        - ``Returns`` the selected values in the order stdout, stderr, exit code.
          A single value is returned as is, several as a tuple, none as None

        - ``Raises`` RuntimeError if the device is not alive or the command
          could not be run

        Example:
        | ${out} | Execute Command | controller | uname -a |
        | ${out} | ${err} | Execute Command | controller | cat /etc/os-release | return_stderr=True |
        | ${rc} | Execute Command | extender1 | reboot | return_stdout=False | return_rc=True |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        out = connection_obj.execute_command(device,
                                             command,
                                             return_stdout = return_stdout,
                                             return_stderr = return_stderr,
                                             return_rc = return_rc,
                                             timeout = timeout,
                                             blocking_call = blocking_call)
        return out

    @keyword("Close Connection")
    def close_connection(self,
                         device: str):
        """
        Close the connection to the device.

        Does nothing if ``device_present`` of the device is False.

        - ``device`` is the device name as defined in the infra.yaml config file

        Example:
        | Close Connection | controller |
        """
        zi_logger.print_context()
        state = self.db_obj.read_from_database(device, 'device_present')
        zi_logger.log(f"{device} state: {state}")
        if state:
            connection = self.db_obj.read_device_connection(device)
            connection_obj = self.get_connection_module_object(connection)
            connection_obj.close_connection(device)

    @keyword("Get File")
    def get_file(self,
                 device: str,
                 source: str,
                 destination: str):
        """
        Copy a file from the device to the local machine (SSH only).

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``source`` is the file path on the device

        - ``destination`` is the local file path

        - ``Raises`` RuntimeError if the file could not be copied

        Example:
        | Get File | controller | /tmp/log.txt | /home/user/log.txt |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.get_file(device, source, destination)

    @keyword("Put File")
    def put_file(self,
                 device: str,
                 source: str,
                 destination: str):
        """
        Copy a file from the local machine to the device (SSH only).

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``source`` is the local file path

        - ``destination`` is the file path on the device

        - ``Raises`` Exception if the file could not be copied

        Example:
        | Put File | controller | /home/user/config.txt | /tmp/config.txt |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.put_file(device, source, destination)
