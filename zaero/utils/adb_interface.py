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
This module handles various adb device.

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
    AdbInterface handles communication with Android devices via ADB(USB).
    """
    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()

    def start_adb_server(self):
        """Start the ADB server.

        Raises:
            RuntimeError: If the ADB server fails to start.

        Examples:
        | Start Adb server |

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
        """kill the ADB server.

        ``Raises``:
            ``RuntimeError``: If the ADB server fails to kill.

        Examples:
        | Kill Adb server |

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
        Execute an adb command on an ADB-connected device.

        - ``command``: Shell command that must NOT start with 'adb'.
        - ``device_id``: Specific device ID (optional).
        - ``return_stdout``: If True, includes stdout.
        - ``return_rc``: If True, includes return code.
        - ``return_stderr``: If True, includes stderr.

        - Raises:
            ``RuntimeError``: If the command is not running properly.
        
        |Example|
        | Execute Adb Command | device_id=RZCT81F35HJ | command=shell input keyevent 224 |
        | ${stdout}=  Execute Adb Command | device_id=RZCT81F35HJ | command=get-state | # state of default adb device |
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
        Retrieve the android version of given or specific device.

        -``device_id``: Specific device id
        - ``returns``: Returns the android version of given device.
                       For example: 15
        Examples:
        | ${output} | Get Android Version | device_id=RZCT81F35HJ | # ouptut: 14 |

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
        Close on current adb connection
        """
        zi_logger.print_context()
        self.kill_adb_server()
        if self.check_adb_service():
            raise RuntimeError("Adb server doesn't stopped....")
        
    def connect_with_device(self,
                            device: str):
        """
        To connect with a remote device using adb protocol

        ``raise`` Runtime error if could not connect with the given device
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
        Switch the adb connection into the specific device.
        It's a dummy function.
        """
        zi_logger.print_context()

    def check_adb_service(self):
        """
        Ensure that adb service running or not.
        """
        zi_logger.print_context()
        result = subprocess.run(
            'netstat -tuln | grep 5037 | grep LISTEN',
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
