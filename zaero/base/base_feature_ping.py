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
Abstract base class for ping methods.

Author: Zilogic Systems <code@zilogic.com>
"""
from abc import ABC, abstractmethod

class BaseFeaturePing(ABC):
    """
    Abstract methods a platform plugin implements for ping.
    Implemented by zaero.linux.
    """
    @abstractmethod
    def ping_ipv4(self,
                  device: str,
                  dst_ip: str,
                  count: int):
        """
        Ping an IPv4 destination from the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``dst_ip`` is the destination address

        - ``count`` is the number of ping packets to send

        - ``Returns`` the packet loss in percent

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement ping_ipv4()")

    @abstractmethod
    def ping_ipv6(self,
                  device: str,
                  dst_ip: str,
                  count: int):
        """
        Ping an IPv6 destination from the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``dst_ip`` is the destination address

        - ``count`` is the number of ping packets to send

        - ``Returns`` the packet loss in percent

        - ``Raises`` NotImplementedError if the subclass does not implement it
        """
        raise NotImplementedError("Subclass must implement ping_ipv6()")
