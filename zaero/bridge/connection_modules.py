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
Factory for the connection modules (SSH, ADB and serial).

Author: Zilogic Systems <code@zilogic.com>
"""

from zaero.utils.ssh_interface import SshInterface
from zaero.utils.adb_interface import AdbInterface
from zaero.utils.serial_interface import SerialInterface
import zaero.utils.zi_logger as zi_logger

class ConnectionModules:
    """
    Singleton factory that returns the connection object for a connection
    type. Supported types are ``ssh`` (SshInterface), ``adb`` (AdbInterface)
    and ``serial`` (SerialInterface). One object is created per type and
    shared by all devices that use it.
    """

    __instance = None
    __modules = {'ssh': SshInterface, 'adb': AdbInterface, 'serial': SerialInterface}
    __module_objects = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            zi_logger.log("ConnectionModules Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.print_context()

    def get_connection_module_object(self, module):
        """
        Get the connection object for the given connection type, creating it on
        first use.

        - ``module`` is the connection type: ``ssh``, ``adb`` or ``serial``,
          as given in the ``connection`` field of the device

        - ``Returns`` the shared connection object

        - ``Raises`` KeyError if the connection type is not supported
        """
        zi_logger.print_context()
        if module not in ConnectionModules.__module_objects:
            zi_logger.log(f"ConnectionModules.modules : {ConnectionModules.__modules}")
            ConnectionModules.__module_objects[module] = ConnectionModules.__modules[module]()
        return ConnectionModules.__module_objects[module]
