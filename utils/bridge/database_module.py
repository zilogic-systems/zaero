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
from zaero.utils.database import Database
import zaero.utils.zi_logger as zi_logger

class DatabaseModule:

    __instance = None
    __module_object = None

    def __new__(cls, *args, **kwargs):
        zi_logger.print_context()
        if cls.__instance is None:
            zi_logger.log("DatabaseModule Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.print_context()

    def get_database_module_object(self):
        zi_logger.print_context()
        if DatabaseModule.__module_object is None:
             DatabaseModule.__module_object = Database()
        return DatabaseModule.__module_object
