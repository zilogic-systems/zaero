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
Author: Zilogic Systems <code@zilogic.com>
"""


from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.platform_modules import PlatformModules
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger

class OperatingSystem(DatabaseModule,
                      PlatformModules):
  

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    
    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        PlatformModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("OperatingSystem __init__ : END")

    @keyword("Get OpenWrt Version")
    def get_openwrt_version(self,
                              device: str) -> str:
        """
        Get the OpenWrt version string from the device
        by reading /etc/openwrt_version.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``Returns`` the OpenWrt version string (e.g., 21.02.3)

        Example:
        | ${ret} | Get OpenWrt Version | ap |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        version = platform_obj.get_openwrt_version(device)
        return version

    @keyword("Get OS Release")
    def get_os_release(self,
                       device: str):
        """
        Get the OS release information from the device
        by reading /etc/os-release.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``Returns`` the contents of /etc/os-release as a string

        Example:
        | ${ret} | Get OS Release | ap |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        release = platform_obj.get_os_release(device)
        return release

    @keyword("Get Kernel Version")
    def get_kernel_version(self,
                         device: str):
        """
        Get the kernel version information from the device via uname -a.

        - ``device`` is the name given to the ap as mentioned
                     in the dut.yaml config file

        - ``Returns`` the full uname output string including kernel version

        Example:
        | ${ret} | Get Kernel Version | ap |
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        kernel = platform_obj.get_kernel_version(device)
        return kernel

