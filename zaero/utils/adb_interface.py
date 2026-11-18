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

"""
ADB connection module. Runs ``adb`` commands on the local machine.

Author: Zilogic Systems <code@zilogic.com>
"""
# Local libraries
from zaero.base.base_adb_interface import BaseAdbInterface

# Standard libraries
import subprocess
import time

# Third party libraries
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger


class AdbInterface(BaseAdbInterface):
    """
    Connection module for Android devices over ADB. Used for devices with
    ``connection: 'adb'``.
    """
    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()

    def start_adb_server(self):
        """
        Start the ADB server with ``adb start-server``.

        - ``Raises`` RuntimeError if adb is not installed or the command fails
        """
        zi_logger.print_context()
        try:
            result = subprocess.run(
                ["adb", "start-server"],
                capture_output=True,
                text=True,
                check=True
            )
            zi_logger.log(f"result: {result.returncode}")
        except FileNotFoundError as e:
            raise RuntimeError("ADB command not found. Make sure Android SDK is installed and in PATH") from e
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ADB start-server failed: {e.stderr.strip()}") from e

    def kill_adb_server(self):
        """
        Stop the ADB server with ``adb kill-server``.

        - ``Raises`` RuntimeError if adb is not installed or the command fails
        """
        zi_logger.print_context()
        try:
            result = subprocess.run(
                ["adb", "kill-server"],
                capture_output=True,
                text=True,
                check=True
            )
        except FileNotFoundError as e:
            raise RuntimeError("ADB command not found. Make sure Android SDK is installed and in PATH") from e
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"ADB stop-server failed: {e.stderr.strip()}") from e
        
    @keyword("Execute Command")
    def execute_command(self,
                        device_id: str,
                        command:str,
                        return_stdout=True,
                        return_rc=False,
                        return_stderr=False):
        """
        Run ``adb -s <device_id> <command>`` on the local machine, after a
        5 second delay.

        Note: this signature differs from the SSH and serial modules. It takes
        ``device_id`` instead of ``device`` and has no ``timeout`` or
        ``blocking_call`` arguments.

        - ``device_id`` is the ADB serial number of the device

        - ``command`` is the adb command without the leading ``adb``,
          e.g. ``shell uname``

        - ``return_stdout`` if True, return the stdout (default: True)

        - ``return_rc`` if True, return the exit code (default: False)

        - ``return_stderr`` if True, return the stderr (default: False)

        - ``Returns`` the selected values in the order stdout, exit code,
          stderr. A single value is returned as is, several as a list, none
          as None

        - ``Raises`` RuntimeError if the command could not be run

        Example:
        | ${out} | Execute Command | RZCT81F35HJ | shell input keyevent 224 |
        | ${out} | ${err} | Execute Command | RZCT81F35HJ | get-state | return_stderr=True |
        """
        zi_logger.print_context()        
        time.sleep(5)
        full_command = f"adb -s {device_id} {command}"
        zi_logger.log(f"Execute Adb Command: {full_command}")
        try:
            process = subprocess.Popen(full_command,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       encoding='UTF-8')
            stdout, stderr = process.communicate()

            response = []
            if return_stdout:
                response.append(stdout.strip())
            if return_rc:
                response.append(process.returncode)
            if return_stderr:
                response.append(stderr.strip())

            return response if len(response) > 1 else response[0] if response else None

        except Exception as err:
            zi_logger.log(f"Could not execute the command - {full_command}", "error")
            raise RuntimeError(f"Command execution failed: {err}")

    def get_android_version(self, device_id: str) -> int:
        """
        Get the Android version with ``adb shell getprop ro.build.version.release``.

        - ``device_id`` is the ADB serial number of the device

        - ``Returns`` the major version as an integer, e.g. ``14``

        - ``Raises`` ValueError if no version is returned
        """
        zi_logger.print_context()
        command = f"shell getprop ro.build.version.release"
        result = self.execute_command(command=command, device_id=device_id)        
        if not result:
            raise ValueError(f"Invalid android version")
        return int(result)

    @keyword("Close Connection")
    def close_connection(self,
                         device: str):
        """
        Stop the ADB server.

        - ``device`` is not used; the server is stopped for all devices

        - ``Raises`` RuntimeError if the server is still running afterwards

        Example:
        | Close Connection | android_client_1 |
        """
        zi_logger.print_context()
        self.kill_adb_server()
        if self.check_adb_service():
            raise RuntimeError("Adb server doesn't stopped....")
        
    def connect_with_device(self,
                            device: str):
        """
        Start the ADB server.

        - ``device`` is the device name, used only in the log message

        - ``Returns`` True if the server is running

        - ``Raises`` RuntimeError if the server could not be started
        """
        zi_logger.print_context()
        
        self.start_adb_server()

        if not self.check_adb_service():
            raise RuntimeError(f"Adb service doesn't started...")
        
        zi_logger.log(f"ADB connection successfully established with the device : {device}")
        return True

    @keyword("Switch Connection")
    def switch_connection(self,
                          alias: str):
        """
        Does nothing. Kept for the BaseAdbInterface API.

        - ``alias`` is not used

        Example:
        | Switch Connection | android_client_1 |
        """
        zi_logger.print_context()

    def check_adb_service(self):
        """
        Check whether the ADB server is listening on port 5037 (``netstat``).

        - ``Returns`` True if it is listening, False otherwise
        """
        zi_logger.print_context()
        result = subprocess.run(
            'netstat -tuln | grep 5037 | grep LISTEN',
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
