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
#from zaero.rdkb import Rdkb
#from zaero.linux import Linux
#from zaero.android import Android
"""
Factory for the platform plugin objects.

Author: Zilogic Systems <code@zilogic.com>
"""

import zaero.utils.zi_logger as zi_logger
import importlib
import inspect

class PlatformModules:
    """
    Singleton factory that loads platform plugins by name. A platform plugin
    is the package ``zaero.<platform>`` containing a class with the same name
    as the package, e.g. ``zaero.linux.linux``. One object is created per
    platform and shared by all devices of that platform.
    """

    __instance = None
    __module_objects = {}

    def __new__(cls, *args, **kwargs):
        zi_logger.print_context()
        if cls.__instance is None:
            zi_logger.log("PlatformModules Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.print_context()

    def get_platform_module_object(self, module):
        """
        Get the object of the given platform plugin, importing the package
        ``zaero.<module>`` and creating the object on first use.

        - ``module`` is the platform name, as given in the ``platform`` field of
          the device, e.g. ``linux`` or ``android``

        - ``Returns`` the platform plugin object

        - ``Raises`` ModuleNotFoundError if the package does not exist and
          Exception if the package has no class with the same name
        """
        zi_logger.print_context()
        if module not in PlatformModules.__module_objects:
            imp_module = importlib.import_module(f"zaero.{module}")
            classes = inspect.getmembers(imp_module, inspect.isclass)
            for name, cls in classes:
                #zi_logger.log(f"****************PM.CLASS NAME : {name}")
                if name == module:
                    PlatformModules.__module_objects[module] = cls()
                    break
            else:
                raise Exception("More than one classes defined in the platform module : {module}")
        return PlatformModules.__module_objects[module]
