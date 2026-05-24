import zaero
import pytest
import time

def test_config_ssid_3(pitstop):
    ssid = pitstop.read_from_database("controller", "mld_ssid_3")
    pitstop.set_ssid("controller", "MLD", ssid)
    for i in range(1, 31):
        try:
            pitstop.check_ssid("controller", "mld_iface_index", ssid)
        except Exception as ERR:
            print(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)

def test_config_ssid_2(pitstop):
    ssid = pitstop.read_from_database("controller", "mld_ssid_2")
    pitstop.set_ssid("controller", "MLD", ssid)
    for i in range(1, 31):
        try:
            pitstop.check_ssid("controller", "mld_iface_index", ssid)
        except Exception as ERR:
            print(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)

def test_config_ssid_1(pitstop):
    ssid = pitstop.read_from_database("controller", "mld_ssid_1")
    pitstop.set_ssid("controller", "MLD", ssid)
    for i in range(1, 31):
        try:
            pitstop.check_ssid("controller", "mld_iface_index", ssid)
        except Exception as ERR:
            print(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)
