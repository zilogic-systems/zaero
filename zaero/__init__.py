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
zaero - test automation library for networking devices such as gateways,
mesh controllers, extenders and WiFi clients.

Import it in Robot Framework with ``Library    zaero`` or use the
``zaero`` class directly from Python.

Author: Zilogic Systems <code@zilogic.com>
"""

from zaero.map.client import Client
from zaero.map.connection import Connection
from zaero.map.database import Database
from zaero.map.ping import Ping
from zaero.map.ui import Ui
from zaero.map.packet_sniffer import PacketSniffer
from zaero.map.packet_capture import PacketCapture
from zaero.map.platform import platform
from zaero.map.pdu import PduControl
from zaero.map.traffic_generator import TrafficGenerator  
import zaero.utils.zi_logger as zi_logger

class zaero(Client,
            Connection,
            Database,
            Ping,
            Ui,
	    PacketSniffer,
            PacketCapture,
            platform,
	    PduControl,
            TrafficGenerator
            ):
    """
    Robot Framework library that combines all zaero keyword groups:
    Client, Connection, Database, Ping, Ui, PacketSniffer, PacketCapture,
    platform, PduControl and TrafficGenerator.

    Every keyword takes a device name defined in the config files loaded by
    `Initialize Database`. The keyword looks up the ``platform`` or
    ``connection`` of that device and dispatches to the matching platform
    plugin or connection module.

    Platform specific keywords from an external plugin are added at run time
    with `Configure Platform`.

    Example:
    | Library             | zaero             |
    | Initialize Database | ${CURDIR}/config |
    | Connect With Device | controller        |
    """

    def __init__(self):
        zi_logger.print_context()
        zi_logger.set_log_state(True)
        zi_logger.log("******* zaero __init__ : START")
        platform.__init__(self)
        Client.__init__(self)
        Connection.__init__(self)
        Database.__init__(self)
        Ping.__init__(self)
        Ui.__init__(self)
        PacketSniffer.__init__(self)
        PacketCapture.__init__(self)
        PduControl.__init__(self)
        TrafficGenerator.__init__(self)    
        zi_logger.log("******* zaero __init__ : END")
