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

import inspect
from pathlib import Path

def print_context():
    frame = inspect.currentframe().f_back

    # Function name
    function_name = frame.f_code.co_name

    # Module name
    module = inspect.getmodule(frame)
    module_name = module.__name__

    #module_name = ".".join(module_name.split('.')[1:])

    # Parent directory
    file_path = Path(module.__file__)
    parent_directory = file_path.parent.name

    parent_directory = ".".join(parent_directory.split('.')[1:])

    # Class name (if inside a class)
    class_name = None
    if 'self' in frame.f_locals:
        class_name = frame.f_locals['self'].__class__.__name__

    # Get function arguments with values
    args_info = inspect.getargvalues(frame)

    args_dict = {
        arg: args_info.locals[arg]
        for arg in args_info.args
        if arg != 'self'
    }

    # Build full name
    if class_name:
        location = f"{parent_directory}.{module_name}.{class_name}.{function_name}"
    else:
        location = f"{parent_directory}.{module_name}.{function_name}"

    print(f"FUNC : {location}({args_dict})")

en_log = True

def log(message):
    if en_log:
        print(f"LOG : {message}")

def enable_log(status):
    global en_log
    en_log = status
