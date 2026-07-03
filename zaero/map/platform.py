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
import importlib
import inspect
from zaero.bridge.database_module import DatabaseModule
import zaero.utils.zi_logger as zi_logger

class platform(DatabaseModule):

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        self.db_obj = self.get_database_module_object()

    @classmethod
    def configure_platform(cls, os_name : str, external=True):
        zi_logger.print_context()
        if external:
            imp_module = importlib.import_module(f"{os_name}")
        else:
            imp_module = importlib.import_module(f"zaero.{os_name}")
        classes = inspect.getmembers(imp_module, inspect.isclass)
        for name, imp_cls in classes:
            #zi_logger.log(f"****************PM.CLASS NAME : {name}")
            if name == os_name and imp_cls.__module__ == imp_module.__name__:
                cls.__bases__ = (imp_cls,) + cls.__bases__
                break
        else:
            raise Exception("Class - {os_name} Not found in the platform module : {os_name}")
