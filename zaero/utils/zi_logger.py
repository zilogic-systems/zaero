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

enable_log = True
enable_api_info = False

def print_context():
    if not enable_api_info:
        return
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

def log(message, status="INFO"):
    if not enable_log:
        return
    if status == "INFO":
        print(f"INFO : {message}")
    else:
        print_error(message)

def set_log_state(status):
    global enable_log
    enable_log = status

def set_api_info(status):
    global enable_api_info
    enable_api_info = status

_error_logs = []

def print_step(message):
    """Log an informational step. Bold white in the console."""
    print(f"\033[1m\033[97m{message}\033[0m")
    return f'<span style="color:black; font-weight:bold;">{message}</span>'

def print_success(message):
    """Log a passing assertion/step. Green in the console, PASS: prefixed."""
    print(f"\033[92m{message}\033[0m")
    return f'<span style="color:green; font-weight:bold;">{message}</span>'

def print_error(message):
    """Log a failing assertion/step. Red in the console, FAIL: prefixed.

    The message is also stored so the active test can be marked as
    failed even when print_error is used instead of raising/asserting.
    """
    print(f"\033[91m{message}\033[0m")
    _error_logs.append(message)
    return f'<span style="color:red; font-weight:bold;">{message}</span>'

def get_error_logs():
    """Return the failure messages logged so far for the current test."""
    return list(_error_logs)

def clear_error_logs():
    """Reset the failure messages. Called automatically before each test
    by the zaero pytest plugin."""
    _error_logs.clear()
