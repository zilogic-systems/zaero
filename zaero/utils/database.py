# Copyright 2024 Zilogic Systems
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
In-memory database that holds the testbed config.

Author: Zilogic Systems <code@zilogic.com>
"""
import random
import string
import json
import os
import yaml
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger

class Database:
    """
    Holds the data of all config files in one dictionary shared by all
    instances. Top-level keys are device names.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    __database = {}

    def __init__(self):
        zi_logger.print_context()

    @keyword("Initialize Database")
    def initialize_database(self,
                            config_dir: str) -> None:
        """
        Load every ``.yaml``, ``.yml`` and ``.json`` file in the directory into
        the database. Sub directories and other files are skipped.

        Files are read in name order. When the same top-level key appears in
        several files, the fields are merged and later files override earlier
        ones.

        - ``config_dir`` is the directory that holds the config files

        - ``Raises`` RuntimeError if the directory or a file could not be read
        """
        zi_logger.print_context()
        try:
            files = os.listdir(config_dir)
            files.sort()
            for file_name in files:
                file_path = os.path.join(config_dir, file_name)
                if os.path.isdir(file_path):
                    continue
                zi_logger.log(f"============YAML file : {file_path}")
                file_type = file_name.split('.')[-1].lower()
                with open(file_path, 'r', encoding="utf-8") as data_file:
                    try:
                        data = ''
                        if file_type in ('yaml', 'yml'):
                            data = yaml.safe_load(data_file)
                        if file_type == 'json':
                            data = json.load(data_file)
                        if data:
                            for key, value in data.items():
                                if key in Database.__database.keys():
                                    Database.__database[key].update(value)
                                else:
                                    Database.__database[key] = value
                            #zi_logger.log(f"DATABASE IS : {Database.__database}")
                    except Exception as err: # pylint: disable=broad-except
                        raise RuntimeError(f"ERROR reading YAML file {file_name}: {err}") from err
        except Exception as err: # pylint: disable=broad-except
            raise RuntimeError(f"ERROR Find Directory {config_dir} : {err}") from err

    @keyword("Read From Database")
    def read_from_database(self,
                           *args: list) -> object:
        """
        Read a value from the database.

        - ``args`` are 1 to 4 keys, followed level by level, e.g.
          ``('controller', 'login_ip')`` returns ``database['controller']['login_ip']``.
          With more than 4 keys, None is returned

        - ``Returns`` the stored value

        - ``Raises`` RuntimeError if a key is not present
        """
        zi_logger.print_context()
        arg_len = len(args)
        data = None
        try:
            if arg_len == 1:
                data = Database.__database[args[0]]
            elif arg_len == 2:
                data = Database.__database[args[0]][args[1]]
            elif arg_len == 3:
                data = Database.__database[args[0]][args[1]][args[2]]
            elif arg_len == 4:
                data = Database.__database[args[0]][args[1]][args[2]][args[3]]
            return data
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"ERROR : {err}", "error")
            raise RuntimeError(f"Could not fetch data from database dictionary for \
the values {args}") from err

    def write_into_database(self,
                            *args: list) -> None:
        """
        Write a value into the database.

        - ``args`` are 2 to 4 keys followed by the value, e.g.
          ``('controller', 'connection_status', True)`` sets
          ``database['controller']['connection_status']``. All keys except the
          last must already exist. Other argument counts are ignored

        - ``Raises`` RuntimeError if a key is not present
        """
        zi_logger.print_context()
        arg_len = len(args)
        try:
            if arg_len == 3:
                Database.__database[args[0]][args[1]] = args[2]
            elif arg_len == 4:
                Database.__database[args[0]][args[1]][args[2]] = args[3]
            elif arg_len == 5:
                Database.__database[args[0]][args[1]][args[2]][args[3]] = args[4]
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"ERROR : {err}", "error")
            raise RuntimeError(f"Could not write data into database dictionary for \
the values {args}") from err
    

    def get_testbed_devices(self):
        """
        Get the names of the devices with ``device_present`` set to True.

        - ``Returns`` a list of device names
        """
        zi_logger.print_context()
        devices = list(Database.__database.keys())
        device_present = []
        for device in devices:
            try:
                if Database.__database[device]['device_present']:
                    device_present.append(device)
            except:
                continue
        return device_present    

    def get_live_devices(self):
        """
        Get the testbed devices whose ``connection_status`` is True.

        Devices that were never connected have no ``connection_status``
        and are not included.

        - ``Returns`` a list of device names
        """
        zi_logger.print_context()
        devices = self.get_testbed_devices()
        live_devices = [device for device in devices
                        if Database.__database[device].get('connection_status', False)]
        return live_devices

    def get_testbed_platforms(self):
        """
        Get the platforms used by the testbed devices.

        - ``Returns`` a list of platform names without duplicates
        """
        zi_logger.print_context()
        devices = self.get_testbed_devices()
        platforms = []
        for device in devices:
            try:
                platform = Database.__database[device]['platform']
                if platform not in platforms:
                    platforms.append(platform)
            except Exception as err: # pylint: disable=broad-except
                zi_logger.log(f"ERROR: {err}", "error")
                zi_logger.log(f"Could not find out the platform of the device : {device}", "error")
        return platforms

    def read_device_connection(self,
                               device: str):
        """
        Get the ``connection`` type of a device.

        - ``device`` is the device name

        - ``Returns`` the connection type, e.g. ``ssh``

        - ``Raises`` UnboundLocalError if the device has no ``connection`` field
        """
        zi_logger.print_context()
        try:
            connection = Database.__database[device]['connection']
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            zi_logger.log(f"Could not read connection of the device : {device}", "error")
        return connection

    def get_random_ssid(self):
        """
        Generate a random SSID: 4-6 upper case letters, 4-6 lower case letters
        and 2-4 digits.

        - ``Returns`` the SSID
        """
        ssid_cap = "".join(random.choices(string.ascii_uppercase, k=random.randint(4, 6)))
        ssid_low = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 6)))
        ssid_int = "".join(random.choices(string.digits, k=random.randint(2, 4)))
        return ssid_cap + ssid_low + ssid_int
