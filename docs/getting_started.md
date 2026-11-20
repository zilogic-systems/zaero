# Getting Started with Zaero

## Prerequisites

- Python 3.10+ (the package's `pyproject.toml` declares `requires-python = ">=3.10"`)
- pip
- A Linux environment is recommended (SSH/serial/ADB access to a test-bed)

## Installation

Zaero is not currently published to PyPI; you build and install the wheel
from a checkout.

```bash
git clone https://github.com/zilogic-systems/zaero.git
cd zaero

# 1. Build the wheel
python3 -m pip install build
python3 -m build

# 2. Install it
cd dist/
python3 -m pip install zaero-<version>-py3-none-any.whl

# 3. Install the browser drivers used by the `Ui` (Playwright) keywords
playwright install --with-deps
```

This pulls in zaero's runtime dependencies: `robotframework`, `paramiko`
+ `scp` (SSH), `pyserial` (serial console), `PyYAML` (config), `playwright`
(GUI automation) and `pytest`/`pytest_html` (for Python-side test runners).

## Generate a testbed configuration

Zaero ships default config templates inside the package
(`zaero/config/*.yaml`). Copy them into your working directory with:

```bash
python -m zaero init_config
```

This copies every `*.yaml` file bundled under `zaero/config/` (currently
`infra.yaml` — the testbed/device database) into the current directory. If a file with the
same name already exists, you're prompted before it's overwritten.

## Understanding the testbed database

`infra.yaml` is the single source of truth for every device zaero can talk
to. Each top-level key is a device name; its value is a mapping of fields
that the keyword layer reads via `device` name at call time (see
[Architecture](architecture.md#1-testbed-database-zaeroconfigyaml-zaeroutilsdatabasepy)):

```yaml
controller:
    device_present: True                 # Indicates whether the controller device is present in the testbed
    platform: 'rdkbmeshzap'              # Zaero plugin name used for the controller
    connection: 'ssh'                    # Connection method used to access the controller
    ssh_tunnel: False                    # Indicates whether SSH tunneling is required
    wan_iface: 'erouter0'                # WAN interface name of the controller
    login_ip: '172.16.130.159'            # IP address used to connect to the controller
    username: 'root'                     # SSH login username
    password: 'user'                     # SSH login password
    port: 22                             # SSH port number
    serial_port: '/dev/ttyUSB0'          # Serial device port used to access the controller
    serial_baudrate: 115200              # Baud rate used for the serial connection
    pcap_remote_dir: /home/root/pcap_logs # Directory on the controller where packet captures are stored
    pcap_local_dir: /home/sujitha/pcap_logs # Local directory where packet captures are copied

extender1:
    device_present: True                 # Indicates whether extender1 is present in the testbed
    platform: 'rdkbmeshzap'              # Zaero plugin name used for extender1
    connection: 'ssh'                    # Connection method used to access extender1
    ssh_tunnel: True                     # Indicates that SSH tunneling is required for extender1
    tunnel_device: controller            # Device through which the SSH tunnel is established
    login_ip: '10.0.0.64'                # IP address of extender1
    username: 'root'                     # SSH login username
    password: 'user'                     # SSH login password
    port: 22                             # SSH port number
    serial_port: '/dev/ttyUSB1'          # Serial device port used to access extender1
    serial_baudrate: 115200              # Baud rate used for the serial connection

extender2:
    device_present: False                # Indicates whether extender2 is present in the testbed
    platform: 'rdkbmeshzap'              # Zaero plugin name used for extender2
    connection: 'ssh'                    # Connection method used to access extender2
    ssh_tunnel: False                    # Indicates whether SSH tunneling is required
    tunnel_device: controller            # Device through which the SSH tunnel can be established
    login_ip: '10.0.0.223'               # IP address of extender2
    username: 'root'                     # SSH login username
    password: 'user'                     # SSH login password
    port: 22                             # SSH port number
    serial_port: '/dev/ttyUSB1'          # Serial device port used to access extender2
    serial_baudrate: 115200              # Baud rate used for the serial connection
    
extender3:
    device_present: False                # Indicates whether extender3 is present in the testbed
    platform: 'rdkbmeshzap'              # Zaero plugin name used for extender3
    connection: 'ssh'                    # Connection method used to access extender3
    ssh_tunnel: False                    # Indicates whether SSH tunneling is required
    tunnel_device: controller            # Device through which the SSH tunnel can be established
    login_ip: '10.0.0.11 '               # IP address of extender3
    username: 'root'                     # SSH login username
    password: 'user'                     # SSH login password
    port: 22                             # SSH port number
    serial_port: '/dev/ttyUSB1'          # Serial device port used to access extender3
    serial_baudrate: 115200              # Baud rate used for the serial connection

controller_lan_client_1:
    device_present: False                # Indicates whether the controller LAN client is present
    platform: 'linux'                    # Platform type of the LAN client
    connection: 'ssh'                    # Connection method used to access the LAN client
    login_ip: '10.0.0.22'                # IP address of the LAN client
    username: 'root'                     # SSH login username
    password: 'user'                     # SSH login password
    port: 22                             # SSH port number
    data_iface: 'enp3s0'                 # Network interface used for LAN data traffic
    mac: 11:22:33:44:55:66               # MAC address of the LAN client

controller_wlan_client_1:
    device_present: True                # Indicates whether the controller WLAN client is present
    platform: 'linux'                    # Platform type of the WLAN client
    connection: 'ssh'                    # Connection method used to access the WLAN client
    login_ip: '172.16.128.134'           # IP address of the WLAN client
    username: 'root'                     # SSH login username
    password: 'user'                     # SSH login password
    port: 22                             # SSH port number
    data_iface: 'wlp113s0'               # Wireless network interface used for WLAN traffic
    mac: 70:1a:b8:82:86:29               # MAC address of the WLAN client
    ssh_tunnel: False                    # Indicates whether SSH tunneling is required

```

A few conventions worth knowing:

- `device_present: False` lets you keep a device's definition in the file
  without including it in a run — `Connect With Device` and
  `Close Connection` both check this flag and skip silently if it's unset.
  `Get Testbed Devices` returns only devices where it's `True`.
  `Database.get_live_devices()` further filters that list down to devices
  whose `connection_status` is currently `True` (i.e. actually reachable).
- `ssh_tunnel` / `tunnel_device` chain a device's SSH session through
  another device that's already connected — used for mesh extenders that
  are only reachable via the controller.
- `platform` must match either an in-tree module under `zaero/` (`linux`,
  `android`) or the importable name of a separately installed plugin
  package (see [Development](development.md)).
- Client devices additionally need `data_iface` (the Wi-Fi/Ethernet
  interface keywords operate on) and Android devices need `device_id`
  (read via ADB).

## Running keywords from Robot Framework

```robotframework
*** Settings ***
Library    zaero

*** Test Cases ***
Client Connects To The AP
    Configure Platform      linux             external=False
    Configure Platform      rdkbmeshzap
    Initialize Database     ${CURDIR}/config

    Connect With Device     ap
    Connect With Device     controller_wlan_client_1

    Set Ssid                ap    2g_radio_index    my_ssid
    Connect Client To Ssid  controller_wlan_client_1    my_ssid    12345678
    ${ssid}=                Get Client Connected Ssid    controller_wlan_client_1
    Should Be Equal          ${ssid}    my_ssid

    ${loss}=                Ping Ipv4    controller_wlan_client_1    8.8.8.8    4
    Should Be Equal As Integers    ${loss}    0
```

Run it the usual way:

```bash
robot suite.robot
```

`Configure Platform` must be called once per platform you use in the suite
**before** `Initialize Database`/`Connect With Device` reference a device
of that platform — it patches the platform's keywords into the `zaero`
library at runtime (see
[Runtime plugin loading](architecture.md#runtime-plugin-loading)).

## Using zaero directly from Python

Because every keyword is a plain method underneath the `@keyword` decorator,
you can drive the same library from a script or `pytest` without Robot
Framework:

```python
from zaero import zaero

z = zaero()
z.initialize_database("./config")
platform = initialize.read_from_database("device","platform")
z.configure_platform(platform)
z.connect_with_device("controller_wlan_client_1")
ip = z.get_client_ipv4("controller_wlan_client_1")
print(ip)
```

This is useful for ad-hoc exploration of a test-bed, or for writing
`pytest`-based test suites that need Python-level control flow around the
same device operations a `.robot` suite would use.
