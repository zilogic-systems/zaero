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
Methods to drive the web UI of a device with Playwright.

These methods are not Robot Framework keywords (they have no
``@keyword`` decorator). They call the ``FeatureUi`` object of the
device's platform, see UiModules.

Author: Zilogic Systems <code@zilogic.com>
"""

from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.ui_modules import UiModules
from robot.api.deco import keyword
import zaero.utils.zi_logger as zi_logger

class Ui(DatabaseModule,
         UiModules):
    """
    Web UI methods. Each method reads the ``platform`` of the device and
    calls the same method on the ``<platform>.feature_ui.FeatureUi`` object.
    """

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        zi_logger.print_context()
        DatabaseModule.__init__(self)
        UiModules.__init__(self)
        self.db_obj = self.get_database_module_object()
        zi_logger.log(f"==== db_obj : {self.db_obj}")
        zi_logger.log("Interface __init__ : END")

    def get_ui_platform_obj(self,
                            device):
        """
        Get the FeatureUi object for the platform of the device.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``Returns`` the FeatureUi object
        """
        zi_logger.print_context()
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_ui_module_object(platform)
        return platform_obj

    def ui_start_playwright(self,
                            device):
        """
        Start Playwright.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_start_playwright()

    def ui_stop_playwright(self,
                           device):
        """
        Stop Playwright.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_stop_playwright()

    def ui_open_browser(self,
                        device):
        """
        Open a browser.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_open_browser()

    def ui_close_browser(self,
                        device):
        """
        Close the browser.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_close_browser()

    def ui_open_context(self,
                        device):
        """
        Open a new browser context.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_open_context()

    def ui_close_context(self,
                        device):
        """
        Close the browser context.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_close_context()

    def ui_open_page(self,
                     device):
        """
        Open a new page in the browser context.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_open_page()

    def ui_close_page(self,
                     device):
        """
        Close the page.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_close_page()

    def ui_navigate_to_home_page(self,
                                 device):
        """
        Open the home page of the device web UI.

        - ``device`` is the device name as defined in the infra.yaml config file
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_navigate_to_home_page(device)

    def ui_navigate_to_required_page(self,
                                     device,
                                     page):
        """
        Open the given page of the device web UI.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``page`` is the page to open, as understood by the platform's FeatureUi
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_navigate_to_required_page(page)

    def ui_update_input_and_save(self,
                                 device,
                                 profile,
                                 field,
                                 value):
        """
        Set an input field on the current page and save it.

        - ``device`` is the device name as defined in the infra.yaml config file

        - ``profile`` is the profile or section that holds the field

        - ``field`` is the field to update

        - ``value`` is the new value
        """
        zi_logger.print_context()
        obj = self.get_ui_platform_obj(device)
        obj.ui_update_input_and_save(profile, field, value)
        
