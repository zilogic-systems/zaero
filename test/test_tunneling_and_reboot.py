import zaero
import pytest
import time
import os

def test_wifi_reset(initialize: zaero.zaero):
    initialize.wifi_reset("controller", 'gui')
    initialize.reboot_device("extender1", "cli")
    time.sleep(5)
    initialize.reboot_device("controller", "cli")
    initialize.close_connection("controller")
    initialize.close_connection("extender1")
    time.sleep(10)

    for i in range(1, 41):
        print (f"FOR loop iteration : {i}")
        try:
            initialize.connect_with_device("controller")
        except:
            print("Connection FAILED with 'Controller'")
        else:
            print("Connection SUCCESS with 'Controller'")
            break
        time.sleep(10)

    for i in range(1, 41):
        print (f"FOR loop iteration : {i}")
        try:
            initialize.connect_with_device("extender1")
        except:
            print("Connection FAILED with 'Extender1'")
        else:
            print("Connection SUCCESS with 'Extender1'")
            break
        time.sleep(10)

    ssid = initialize.read_from_database("controller", "default_ssid")
    for i in range(1, 31):
        try:            
            initialize.check_ssid("controller", "mld_iface_index", ssid, 'cli')
            initialize.check_ssid("extender1", "mld_iface_index", ssid, 'cli')
        except Exception as err:
            print(err)
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)
