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
    """A library to providing keywords to read all the parameters from config files"""

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    __database = {}

    def __init__(self):
        zi_logger.print_context()

    @keyword("Initialize Database")
    def initialize_database(self,
                            config_dir: str) -> None:
        """
        Read each parameter and its value from all the config files present in
        the given directory and save a dictionary in the class variable ``database``

        It provide support to read data of .yaml and .json file format.

        ``config_dir`` is the directory under which all the config files are stored

        ``raise`` exceptions when the given directory is not present or could not
        open or read any config file present under the directory

        Example:
        | Initialize Database | /tmp/config_dir/ |
        | Initialize Database | ${CONFIG_DIR}    |

        In the second example, we pass the path value stored in a the variable
        ${CONFIG_DIR} as argument to this keyword
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
        Read data from the ``database`` dictionary

        ``args`` define how many layers we need to travel in the database
        dictinary to fetch the required data

        ``raise`` exception if given key is not present in the dictionary

        Example:
        |
        |if the *args are -> 'ap', 'username'
        |data to be returned is,
        |    database['ap']['username']
        |
        |if the *args are -> 'ap', 'radio', 'index'
        |data to be returned is,
        |    database['ap']['radio']['index']
        |
        """
        zi_logger.print_context()
        arg_len = len(args)
        data = None
        try:
            if arg_len == 2:
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
        Returns name of the list of devices present in config files
        """
        zi_logger.print_context()
        #return list(Database.__database.keys())
        devices = list(Database.__database.keys())
        device_present = [device for device in devices if Database.__database[device]['device_present']]
        return device_present    

    def get_live_devices(self):
        """
        Returns name of the list of devices present in config files
        """
        zi_logger.print_context()
        devices = self.get_testbed_devices()
        live_devices = [device for device in devices if Database.__database[device]['connection_status']]
        return live_devices

    def get_testbed_platforms(self):
        """
        Returns each device's platform as list
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
        Returns each device's platform as list
        """
        zi_logger.print_context()
        try:
            connection = Database.__database[device]['connection']
        except Exception as err: # pylint: disable=broad-except
            zi_logger.log(f"ERROR: {err}", "error")
            zi_logger.log(f"Could not read connection of the device : {device}", "error")
        return connection

    def get_random_ssid(self):
        ssid_cap = "".join(random.choices(string.ascii_uppercase, k=random.randint(4, 6)))
        ssid_low = "".join(random.choices(string.ascii_lowercase, k=random.randint(4, 6)))
        ssid_int = "".join(random.choices(string.digits, k=random.randint(2, 4)))
        return ssid_cap + ssid_low + ssid_int
