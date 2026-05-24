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
from zaero.linux.feature_client import FeatureClient
from zaero.linux.feature_ping import FeaturePing
import zaero.utils.zi_logger as zi_logger

class Linux(FeatureClient,
            FeaturePing):
    
    def __init__(self):
        zi_logger.print_context()
        FeatureClient.__init__(self)
        FeaturePing.__init__(self)
        zi_logger.log("Linux __init__ : END")

        
