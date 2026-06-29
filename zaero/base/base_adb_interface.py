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
This module handles various adb device.

Author: Zilogic Systems <code@zilogic.com>
"""
# Third party libraries
from abc import ABC, abstractmethod


class BaseAdbInterface(ABC):
    """ This module provide abstract class for the APIs in one of the adb connections"""
    @abstractmethod
    def start_adb_server(self):
        """ Start an adb server"""
        raise NotImplementedError(
            "Subclass must implement start_adb_server()")

    @abstractmethod
    def kill_adb_server(self):
        """Kill adb server"""
        raise NotImplementedError(
            "Subclass must implement kill_adb_server()")

    @abstractmethod
    def execute_command(self,
                        device_id: str,
                        command:str,
                        return_stdout=True,
                        return_rc=False,
                        return_stderr=False):
        """Execute adb command"""
        raise NotImplementedError(
            "Subclass must implement execute_command()")

    @abstractmethod
    def get_android_version(self, device_id):
        """Get android version"""
        raise NotImplementedError(
            "Subclass must implement get_android_version()")

    @abstractmethod
    def close_connection(self, device: str):
        """ Close Current adb connection"""
        raise NotImplementedError(
            "Subclass must implement close_connection()")
    
    @abstractmethod
    def connect_with_device(self, device: str):
        """ To connect with a remote device using adb protocol """
        raise NotImplementedError(
            "Subclass must implement connect_with_device()")

    @abstractmethod
    def switch_connection(self, alias: str):
        """ Switch the adb connection to a specific device abstract method"""
        raise NotImplementedError(
            "Subclass must implement switch_connection()")

    @abstractmethod
    def check_adb_service(self):
        """ Check whether adb service is running abstract method"""
        raise NotImplementedError(
            "Subclass must implement check_adb_service()")
