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
#from zaero.utils.ui.rdkb_ui import RdkbUi
#from zaero.rdkb.feature_ui import RdkbUi
import zaero.utils.zi_logger as zi_logger
import importlib
import inspect

class UiModules:

    __instance = None
    #__modules = {'rdkb' : RdkbUi}
    __module_objects = {}

    def __new__(cls, *args, **kwargs):
        zi_logger.print_context()
        if cls.__instance is None:
            zi_logger.log("bridge.ui_modules.UiModules Instance created")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        zi_logger.print_context()

    def get_ui_module_object(self, module):
        zi_logger.print_context()
        if module not in UiModules.__module_objects:
            imp_module = importlib.import_module(f"{module}.feature_ui")
            classes = inspect.getmembers(imp_module, inspect.isclass)
            for name, cls in classes:
                print(f"****************PM.CLASS NAME : {name}")
                if name == 'FeatureUi':
                    UiModules.__module_objects[module] = cls()
                    break
            else:
                raise Exception("More than one classes defined in the ui module : {module}")
        return UiModules.__module_objects[module]

