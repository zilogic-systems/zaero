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
This module handles various client operation

Author: Zilogic Systems <code@zilogic.com>
"""
# Third-party Libraries
from robot.api.deco import keyword
from robot.api import SkipExecution

# Local Libraries
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger

class Connection(DatabaseModule,
                 ConnectionModules):
    """
    Provides keywords to establish connections with different devices
    which using different connection types (SSH, ADB, Serial)
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
        Establish a remote connection with the specified device.
        Skips execution if the device is marked as not present in the database.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        - ``Raises`` SkipExecution if the connection cannot be established

        Example:
        | Connect With Device | ap             |
        | Connect With Device | ap_lan_client_1 |
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
            #return status
            if not status:
                raise SkipExecution(
                    f"Could not established remote connection with device: {device}")

    @keyword("Is Device Alive")
    def is_device_alive(self,
                        device: str):
        """
        Check whether the remote connection to the device is still active.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        - ``Returns`` True if the device is reachable, False otherwise

        Example:
        | ${ret} | Is Device Alive | ap              |
        | ${ret} | Is Device Alive | ap_lan_client_1 |
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
                        blocking_call:bool =True):
        """
        Execute a shell command on the specified device and return the requested output.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        - ``command`` is the shell command to run on the device

        - ``return_stdout`` if True, include stdout in the return value (default: True)

        - ``return_stderr`` if True, include stderr in the return value (default: False)

        - ``return_rc`` if True, include the return code in the return value (default: False)

        - ``blocking_call`` if True, wait for the command to finish (default: True)

        - ``Returns`` stdout, stderr, and/or return code depending on the flags set

        Example:
        | ${out} | Execute Command | ap | uname -a |
        | ${out} | ${err} | Execute Command | ap | cat /etc/os-release | return_stderr=True |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        out = connection_obj.execute_command(command,
                                             return_stdout,
                                             return_stderr,
                                             return_rc,
                                             blocking_call)
        return out

    @keyword("Switch To Connection")
    def switch_connection(self,
                          device: str):
        """
        Switch the active connection context to the specified device so that
        subsequent commands are directed to it.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        Example:
        | Switch To Connection | ap              |
        | Switch To Connection | ap_lan_client_1 |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.switch_connection(device)   

    @keyword("Close Connection")
    def close_connection(self,
                         device: str):
        """
        Close the remote connection to the specified device.
        Skips if the device is marked as not present in the database.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        Example:
        | Close Connection | ap              |
        | Close Connection | ap_lan_client_1 |
        """
        zi_logger.print_context()
        state = self.db_obj.read_from_database(device, 'device_present')
        zi_logger.log(f"State: {state}")
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
        Download a file from the remote device to the local machine.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        - ``source`` is the full path of the file on the remote device

        - ``destination`` is the local path where the file will be saved

        Example:
        | Get File | ap | /tmp/log.txt | /home/user/log.txt |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.get_file(source, destination)

    @keyword("Put File")
    def put_file(self,
                 device: str,
                 source: str,
                 destination: str):
        """
        Upload a file from the local machine to the remote device.

        - ``device`` is the name given to the device as mentioned
                     in the dut.yaml config file

        - ``source`` is the local path of the file to upload

        - ``destination`` is the full path on the remote device where the file will be placed

        Example:
        | Put File | ap | /home/user/config.txt | /tmp/config.txt |
        """
        zi_logger.print_context()
        connection = self.db_obj.read_device_connection(device)
        connection_obj = self.get_connection_module_object(connection)
        connection_obj.put_file(source, destination)
