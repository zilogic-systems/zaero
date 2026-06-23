import zaero
import pytest
import time

def test_reboot_controller(initialize):
    ssid = initialize.read_from_database("controller", "mld_ssid_2") 
    initialize.set_ssid("controller", "mld_iface_index", ssid, 'gui')
    for i in range(1, 31):
        try:
            initialize.check_ssid("controller", "mld_iface_index", ssid, "cli")
        except Exception as err:
            print(err)
        else:
            break
        time.sleep(5)
    initialize.reboot_device("controller", "cli")
    initialize.close_connection("controller")
    time.sleep(10)
    for i in range(1, 41):
        print (f"FOR loop iteration : {i}")
        try:
            initialize.connect_with_device("controller")
        except:
            print("Connection FAILED")
        else:
            print("Connection SUCCESS and else part executed")
            break
        time.sleep(10)

    for i in range(1, 31):
        try:
            initialize.check_ssid("controller", "mld_iface_index", ssid, "cli")
        except Exception as err:
            print(err)
        else:
            break
        time.sleep(10)
