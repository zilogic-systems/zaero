import zaero
import pytest
import time

def test_config_ssid(initialize):
    ssid = initialize.read_from_database("controller", "mld_ssid_3")
    initialize.set_ssid("controller", "mld_iface_index", ssid)
    for i in range(1, 31):
        try:
            initialize.check_ssid("controller", "mld_iface_index", ssid)
        except Exception as ERR:
            print(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)
