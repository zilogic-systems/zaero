import zaero
import pytest
import time
import os

def test_config_ssid_with_extenders(initialize):
    ssid = initialize.read_from_database("controller", "mld_ssid_2")
    initialize.set_ssid("controller", "mld_iface_index", ssid, 'gui')
    for i in range(1, 31):
        try:            
            initialize.check_ssid("controller", "mld_iface_index", ssid, 'cli')
            initialize.check_ssid("extender1", "mld_iface_index", ssid, 'cli')
            initialize.check_ssid("extender2", "mld_iface_index", ssid, 'cli')
        except Exception as err:
            print(err)
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)
