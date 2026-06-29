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
from zaero.bridge.database_module import DatabaseModule
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger

class Database(DatabaseModule):

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Map - Database __init__ : END")

    @keyword("Initialize Database")
    def initialize_database(self, config_path):
        """
        Load the testbed configuration file into the in-memory database.

        - ``config_path`` is the path to the YAML or JSON testbed config file

        Example:
        | Initialize Database | ${CURDIR}/config/rdkb/dut.yaml |
        """
        zi_logger.print_context()
        self.db_obj.initialize_database(config_path)

    @keyword("Read From Database")
    def read_from_database(self, *args):
        """
        Read a value from the in-memory testbed database.

        - Pass two arguments (device, key) to read a specific field.
        - Pass one argument to read all fields for a device.

        - ``Returns`` the stored value for the given device and key

        Example:
        | ${val} | Read From Database | ap | platform   |
        | ${val} | Read From Database | ap | connection |
        """
        zi_logger.print_context()
        ret = self.db_obj.read_from_database(*args)
        return ret

    @keyword("Write Into Database")
    def write_into_database(self, *args):
        """
        Write a value into the in-memory testbed database.

        - Pass three arguments (device, key, value) to write a top-level field.
        - Pass four arguments (device, key1, key2, value) to write a nested field.

        Example:
        | Write Into Database | ap | platform | openwrt        |
        | Write Into Database | ap | radio    | 2g_channel | 6 |
        """
        zi_logger.print_context()
        ret = self.db_obj.write_into_database(*args)
        return ret

    @keyword("Get Testbed Devices")
    def get_testbed_devices(self):
        """
        Retrieve the list of all device names defined in the testbed database.

        - ``Returns`` a list of device name strings

        Example:
        | ${devices} | Get Testbed Devices |
        """
        zi_logger.print_context()
        devices = self.db_obj.get_testbed_devices()
        return devices
