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
Abstract base class for operating system information methods.

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod


class BaseFeatureOperatingSystem(ABC):
    """
    Abstract methods a platform plugin implements for operating system information.
    Implemented by external platform plugins.
    """

    @abstractmethod
    def get_openwrt_version(self, device: str):
        """
        Get the OpenWrt version of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the version string

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_openwrt_version()")

    @abstractmethod
    def get_os_release(self, device: str):
        """
        Get the OS release of the device, e.g. from /etc/os-release.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the OS release

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_os_release()")

    @abstractmethod
    def get_kernel_version(self, device: str):
        """
        Get the kernel version of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the kernel version

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement get_kernel_version()")
