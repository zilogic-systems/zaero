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
Console logger used across zaero.

``log`` prints INFO messages when logging is enabled. ``print_context``
prints the calling function and its arguments when API info is enabled.
``print_step``, ``print_success`` and ``print_error`` print coloured
messages; errors are also stored so a test can be failed later.

Author: Zilogic Systems <code@zilogic.com>
"""

import inspect
from pathlib import Path

enable_log = True
enable_api_info = False

def print_context():
    """
    Print the calling function as ``FUNC : <location>(<arguments>)``.

    Does nothing unless API info is enabled with ``set_api_info(True)``.
    """
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

def log(message, status="INFO", log_error= False):
    """
    Print a log message.

    Does nothing if logging is disabled with ``set_log_state(False)``.

    - ``message`` is the text to print

    - ``status`` is ``INFO`` to print ``INFO : <message>``; any other value
      prints the message in red with `print_error`

    - ``log_error`` if True and ``status`` is not ``INFO``, also store the
      message in the error log
    """
    if not enable_log:
        return
    if status == "INFO":
        print(f"INFO : {message}")
    else:
        print_error(message, log_error)

def set_log_state(status):
    """
    Enable or disable `log` messages.

    - ``status`` True to enable, False to disable
    """
    global enable_log
    enable_log = status

def set_api_info(status):
    """
    Enable or disable the function trace printed by `print_context`.

    - ``status`` True to enable, False to disable
    """
    global enable_api_info
    enable_api_info = status

_error_logs = []

def print_step(message):
    """
    Print an informational step in bold white.

    - ``message`` is the text to print

    - ``Returns`` the message as an HTML span in bold black
    """
    print(f"\033[1m\033[97m{message}\033[0m")
    return f'<span style="color:black; font-weight:bold;">{message}</span>'

def print_success(message):
    """
    Print a success message in green.

    - ``message`` is the text to print

    - ``Returns`` the message as an HTML span in bold green
    """
    print(f"\033[92m{message}\033[0m")
    return f'<span style="color:green; font-weight:bold;">{message}</span>'

def print_error(message, log_error=True):
    """
    Print an error message in red and optionally store it, so a test can be
    marked as failed without raising.

    - ``message`` is the text to print

    - ``log_error`` if True (default), store the message in the error log
      returned by `get_error_logs`

    - ``Returns`` the message as an HTML span in bold red
    """
    print(f"\033[91m{message}\033[0m")
    if log_error:
        _error_logs.append(message)
    return f'<span style="color:red; font-weight:bold;">{message}</span>'

def get_error_logs():
    """
    Get the error messages stored by `print_error`.

    - ``Returns`` a copy of the list of stored messages
    """
    return list(_error_logs)

def clear_error_logs():
    """Clear the error messages stored by `print_error`."""
    _error_logs.clear()
