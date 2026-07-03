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
from zaero.map.client import Client
from zaero.map.connection import Connection
from zaero.map.database import Database
import zaero.utils.zi_logger as zi_logger
from zaero.map.ping import Ping
from zaero.map.operating_system import OperatingSystem
from zaero.map.ui import Ui
from zaero.map.packet_sniffer import PacketSniffer
from zaero.map.platform import platform

class zaero(Client,
            Connection,
            Database,
            Ping,
            OperatingSystem,
            Ui,
	    PacketSniffer,
            platform):

    def __init__(self):
        zi_logger.print_context()
        zi_logger.set_log_state(True)
        zi_logger.log("******* zaero __init__ : START")
        platform.__init__(self)
        Client.__init__(self)
        Connection.__init__(self)
        Database.__init__(self)
        Ping.__init__(self)
        OperatingSystem.__init__(self)
        Ui.__init__(self)
        PacketSniffer.__init__(self)
        zi_logger.log("******* zaero __init__ : END")
