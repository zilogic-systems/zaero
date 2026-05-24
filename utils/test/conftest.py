import zaero
import zaero.utils.zi_logger as zi_logger
import pytest
import time

@pytest.fixture(scope='session', autouse=True)
def pitstop():
    zi_logger.log(f"test.conftest.pitsop()")
    obj = zaero.zaero()
    obj.initialize_database("/home/manikandan/manikandan/projects/RDK-M/pitstop-rdkb-em/config/rdkb")
    obj.connect_with_device("controller")
    obj.ui_start_playwright("controller")
    time.sleep(1)
    obj.ui_open_browser("controller")
    time.sleep(1)
    yield obj
    obj.ui_close_browser("controller")
    obj.ui_stop_playwright("controller")
    del(obj)

@pytest.fixture(scope='function', autouse=True)
def test_setup(pitstop):
    zi_logger.log(f"test.conftest.test_setup()")
    pitstop.ui_open_context("controller")
    time.sleep(1)
    pitstop.ui_open_page("controller")
    time.sleep(1)
    yield pitstop
    pitstop.ui_close_page("controller")
    pitstop.ui_close_context("controller")
