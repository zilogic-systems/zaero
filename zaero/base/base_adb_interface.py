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
Abstract base class for ADB connection methods.

Author: Zilogic Systems <code@zilogic.com>
"""
# Third party libraries
from abc import ABC, abstractmethod


class BaseAdbInterface(ABC):
    """
    Abstract methods a platform plugin implements for ADB connection.
    Implemented by zaero.utils.adb_interface.AdbInterface.
    """
    @abstractmethod
    def start_adb_server(self):
        """
        Start the ADB server.

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement start_adb_server()")

    @abstractmethod
    def kill_adb_server(self):
        """
        Stop the ADB server.

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement kill_adb_server()")

    @abstractmethod
    def execute_command(self,
                        device_id: str,
                        command:str,
                        return_stdout=True,
                        return_rc=False,
                        return_stderr=False):
        """
        Run an adb command on the device.

        - ``device_id`` is the ADB serial number of the device

        - ``command`` is the adb command without the leading ``adb``

        - ``return_stdout`` if True, return the stdout

        - ``return_rc`` if True, return the exit code

        - ``return_stderr`` if True, return the stderr

        - ``Returns`` the selected outputs in the order stdout, exit code, stderr

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement execute_command()")

    @abstractmethod
    def get_android_version(self, device_id):
        """
        Get the Android version of the device.

        - ``device_id`` is the ADB serial number of the device

        - ``Returns`` the major version as an integer

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement get_android_version()")

    @abstractmethod
    def close_connection(self, device: str):
        """
        Close the ADB connection.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement close_connection()")
    
    @abstractmethod
    def connect_with_device(self, device: str):
        """
        Connect to the device over ADB.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` True if connected

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement connect_with_device()")

    @abstractmethod
    def switch_connection(self, alias: str):
        """
        Switch the active ADB connection to another device.

        - ``alias`` is the connection name

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement switch_connection()")

    @abstractmethod
    def check_adb_service(self):
        """
        Check whether the ADB server is running.

        - ``Returns`` True if running

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError(
            "Subclass must implement check_adb_service()")
