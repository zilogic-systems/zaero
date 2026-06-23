import zaero
import pytest
import time
import os

def test_config_ssid_with_extenders(initialize):
    ssid = initialize.read_from_database("controller", "mld_ssid_3")
    initialize.set_ssid("controller", "mld_iface_index", ssid, 'gui')
    for i in range(1, 31):
        try:            
            initialize.check_ssid("controller", "mld_iface_index", ssid, 'cli')
            initialize.check_ssid("extender1", "mld_iface_index", ssid, 'cli')
            initialize.check_ssid("extender2", "mld_iface_index", ssid, 'cli')
        except Exception as ERR:
            initialize.zi_logger.log(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)

def test_config_ssid_with_packet_capture_and_download(initialize):
    ssid = initialize.read_from_database("controller", "mld_ssid_2")
    pcap_file_name = "sample_6"
    pcap_remote_dir = initialize.read_from_database("controller", "pcap_remote_dir")
    pcap_local_dir = initialize.read_from_database("controller", "pcap_local_dir")
    backhaul_iface = initialize.read_from_database("controller", "backhaul_capture_iface")
    frame_filter = initialize.read_from_database("controller", "filter_1905")

    initialize.set_sniffer_log_file("controller", pcap_file_name)
    initialize.start_frame_capture("controller", backhaul_iface, frame_filter)
    initialize.set_ssid("controller", "mld_iface_index", ssid, 'gui')

    for i in range(1, 31):
        try:
            initialize.check_ssid("controller", "mld_iface_index", ssid, 'cli')
        except Exception as ERR:
            print(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")

    pcap_remote_dir = os.path.join(pcap_remote_dir, pcap_file_name + '.pcapng')
    initialize.download_pcap("controller", pcap_remote_dir, pcap_local_dir)
    initialize.delete_pcap("controller", f"{pcap_file_name}.pcapng")
    time.sleep(10)

def test_config_ssid_with_packet_capture(initialize):
    ssid = initialize.read_from_database("controller", "mld_ssid_3")
    pcap_file_name = "sample_1"
    backhaul_iface = initialize.read_from_database("controller", "backhaul_capture_iface")
    frame_filter = initialize.read_from_database("controller", "filter_1905")
    initialize.set_sniffer_log_file("controller", pcap_file_name)
    initialize.start_frame_capture("controller", backhaul_iface, frame_filter)
    initialize.set_ssid("controller", "mld_iface_index", ssid, 'gui')
    for i in range(1, 31):
        try:            
            initialize.check_ssid("controller", "mld_iface_index", ssid, 'cli')
        except Exception as ERR:
            print(f"ERROR: {ERR}")
        else:
            break
        time.sleep(5)
    else:
        raise Exception("SSID is not changed in DUT by checking with iw command")
    time.sleep(10)

def test_config_ssid(initialize):
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





