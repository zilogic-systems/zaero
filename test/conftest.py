import zaero
import pytest
import time
from pathlib import Path

@pytest.fixture(scope='session', autouse=True)
def initialize():
    zaero_obj = zaero.zaero()
    current_file = Path(__file__)
    current_directory = current_file.parent / "config"
    zaero_obj.initialize_database(current_directory)
    zaero_obj.connect_with_device("controller")
    zaero_obj.ui_start_playwright("controller")
    time.sleep(1)
    zaero_obj.ui_open_browser("controller")
    time.sleep(1)
    yield zaero_obj
    zaero_obj.ui_close_browser("controller")
    zaero_obj.ui_stop_playwright("controller")
    del(zaero_obj)

@pytest.fixture(scope='function', autouse=True)
def test_setup(initialize):
    initialize.ui_open_context("controller")
    time.sleep(1)
    initialize.ui_open_page("controller")
    time.sleep(1)
    yield initialize
    initialize.ui_close_page("controller")
    initialize.ui_close_context("controller")
