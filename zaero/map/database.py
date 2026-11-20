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
Robot Framework keywords to load and access the testbed config data.

Author: Zilogic Systems <code@zilogic.com>
"""

from zaero.bridge.database_module import DatabaseModule
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger

class Database(DatabaseModule):
    """
    Keywords for the in-memory database that holds the testbed config.
    The data is shared by all zaero keywords.
    """

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
        Load every ``.yaml``, ``.yml`` and ``.json`` file in the given directory
        into the database.

        Files are read in name order. When the same top-level key, e.g. a
        device name, appears in several files, the fields are merged and later
        files override earlier ones.

        - ``config_path`` is the directory that holds the config files

        - ``Raises`` RuntimeError if the directory or a file could not be read

        Example:
        | Initialize Database | ${CURDIR}/config |
        """
        zi_logger.print_context()
        self.db_obj.initialize_database(config_path)

    @keyword("Read From Database")
    def read_from_database(self, *args):
        """
        Read a value from the database.

        - ``args`` are 1 to 4 keys, followed level by level.
          One key returns all fields of a device, two keys return one field

        - ``Returns`` the stored value

        - ``Raises`` RuntimeError if a key is not present

        Example:
        | ${data} | Read From Database | controller |
        | ${ip}   | Read From Database | controller | login_ip |
        """
        zi_logger.print_context()
        ret = self.db_obj.read_from_database(*args)
        return ret

    @keyword("Write Into Database")
    def write_into_database(self, *args):
        """
        Write a value into the database.

        - ``args`` are 2 to 4 keys followed by the value. The keys must already
          exist, except the last one

        - ``Raises`` RuntimeError if a key is not present

        Example:
        | Write Into Database | controller | login_ip | 192.168.1.1 |
        | Write Into Database | controller | connection_status | ${False} |
        """
        zi_logger.print_context()
        ret = self.db_obj.write_into_database(*args)
        return ret

    @keyword("Get Testbed Devices")
    def get_testbed_devices(self):
        """
        Get the names of the devices with ``device_present`` set to True.

        - ``Returns`` a list of device names

        Example:
        | ${devices} | Get Testbed Devices |
        """
        zi_logger.print_context()
        devices = self.db_obj.get_testbed_devices()
        return devices

    @keyword("Get Random Ssid")
    def get_random_ssid(self):
        """
        Generate a random SSID: 4-6 upper case letters, 4-6 lower case letters
        and 2-4 digits.

        - ``Returns`` the SSID, e.g. ``KQZTabcde123``

        Example:
        | ${ssid} | Get Random Ssid |
        """
        zi_logger.print_context()
        ssid = self.db_obj.get_random_ssid()
        return ssid
