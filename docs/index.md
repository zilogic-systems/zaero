# Zaero

Zaero is a Python-based test automation framework targeted at testing
networking devices — Access Points, Routers, Mesh/Extender nodes and their
wireless/wired clients (Linux, Android, and beyond).

It is delivered as a single [Robot Framework](https://robotframework.org/)
library (`Library zaero`) that exposes a flat, device-agnostic set of
keywords — `Get Client Ipv4`, `Set Ssid`, `Ping Ipv4`, `Pdu On`, and so on —
that work identically whether the target device is an OpenWrt/RDK-B access
point, a Linux WLAN client, or an Android client. Because the keywords are
plain Python methods under the hood, the same library can be imported and
driven directly from `pytest` or any Python script without Robot Framework
at all.

## Motivation

Wi-Fi/mesh test-beds are heterogeneous by nature: the same test case
("connect a client to an SSID and check the RSSI") has to run unmodified
against an OpenWrt AP, an RDK-B mesh extender, a Linux laptop and an Android
phone — each with a completely different command set (`nmcli` vs `wpa_cli`
vs `uci`) and a different transport (SSH, ADB, serial).

Zaero addresses this by separating **what a test wants to do** (the keyword)
from **how a specific platform does it** (the platform plugin), and from
**how the framework reaches the device** (the connection driver). See
[Architecture](architecture.md) for how these layers fit together.

## Features

- A single Robot Framework library (`zaero`) that aggregates keywords for
  client management, connections, radios, ping, packet
  sniffing/capture and PDU (power) control.
- **Template ABCs** (`zaero/base/`) define the stable contract a platform
  must implement (client ops, radio ops, ping, ADB).
- **Platform plugins** (`zaero/linux/`, `zaero/android/`, and any
  out-of-tree package) implement those templates for a concrete OS/device
  family.
- A **connection layer** (`zaero/utils/ssh_interface.py`,
  `adb_interface.py`, `serial_interface.py`) that abstracts SSH (with
  multi-hop tunnelling), ADB and serial transports behind one small API.
- A YAML/JSON-backed **testbed database** (`Initialize Database`) that maps
  device names to platform, connection type, credentials and per-device
  options — read by every keyword via `device` name, never hard-coded.
- **Runtime-pluggable platforms** — `Configure Platform <name>` can load a
  platform class from inside zaero or from any separately installed Python
  package, and hot-patches it into the running Robot Framework library.
- Keywords double as plain Python methods, so the same library works from
  `pytest`/IPython for ad-hoc scripting, not only from `.robot` suites.

## Installation

```bash
git clone https://github.com/zilogic-systems/zaero.git
cd zaero

python3 -m pip install build
python3 -m build

cd dist/
python3 -m pip install zaero-<version>-py3-none-any.whl

playwright install --with-deps
```

See [Getting Started](getting_started.md) for generating a testbed
configuration and running your first keywords.

## Documentation

- [Getting Started](getting_started.md) — install, generate a testbed
  config, run keywords from Robot Framework or plain Python.
- [Architecture](architecture.md) — the base/platform/bridge/map/utils
  layering and the runtime plugin-loading mechanism.
- [Development](development.md) — how to add a new platform, a new
  keyword module, a new connection type, or a new base template.
- [Keyword Reference](reference/keywords.md) — every keyword exposed by
  the `zaero` library, grouped by category.

## Author

Zilogic Systems
