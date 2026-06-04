import zaero
import pytest
import time

def test_config_ssid_1(initialize):
    ssid = initialize.read_from_database("controller", "mld_ssid_2")
    initialize.set_ssid("controller", "mld_iface_index", ssid, 'gui')
    for i in range(1, 31):
        try:
            initialize.check_ssid("controller", "mld_iface_index", ssid, 'cli')
            curr_ssid = initialize.get_ssid("controller", "2g_ssid_index", 'de')
            if curr_ssid != ssid:
                print(f"Both SSIDs are not matched {ssid} : {curr_ssid}")
        except Exception as ERR:
            print(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)

