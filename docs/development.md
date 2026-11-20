# Development (How-to Guide)

This page walks through extending zaero: adding support for a new
platform, adding a new keyword module, adding a new connection transport,
and adding a new template (base ABC).

## Writing a new platform plugin

Say you want to add support for a `windows` client. Create a package that
mirrors `zaero/linux/`:

```bash
zaero/windows/
├── __init__.py          # exposes `class windows(...)`
└── feature_client.py     # implements BaseFeatureClient
```

### `feature_client.py`

Implement the relevant `base_feature_*` ABC(s) from `zaero/base/`. You do
not have to implement every abstract method of an ABC on day one, but any
method left unimplemented will make the class impossible to instantiate —
so pick the ABCs you actually intend to complete (see
[`base_feature_client.py`](../zaero/base/base_feature_client.py) for the
full `BaseFeatureClient` contract).

```python
# zaero/windows/feature_client.py
from zaero.base.base_feature_client import BaseFeatureClient
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.connection_modules import ConnectionModules
import zaero.utils.zi_logger as zi_logger


class FeatureClient(BaseFeatureClient, DatabaseModule, ConnectionModules):
    """Handles basic WiFi functionality keywords for a Windows client."""

    def __init__(self):
        DatabaseModule.__init__(self)
        ConnectionModules.__init__(self)
        self.db_obj = self.get_database_module_object()

    def get_client_os(self, device: str):
        connection = self.db_obj.read_from_database(device, 'connection')
        connection_obj = self.get_connection_module_object(connection)
        output, error = connection_obj.execute_command(
            device, "ver", return_stderr=True)
        if error:
            raise Exception("Command execution failed: ver")
        return output

    def get_client_ipv4(self, device: str) -> str:
        ...  # e.g. parse `ipconfig` output for the configured interface

    # ... implement the remaining BaseFeatureClient methods
```

### `__init__.py`

The package **must** expose a top-level class whose name is identical to
the package/module name — this is how `PlatformModules` (see
[Architecture](architecture.md#4-bridge--factory-layer-zaerobridgepy))
finds it purely from the `platform:` string in the testbed database:

```python
# zaero/windows/__init__.py
from zaero.windows.feature_client import FeatureClient


class windows(FeatureClient):
    def __init__(self):
        FeatureClient.__init__(self)
```

Reference it from a testbed database entry with `platform: 'windows'`, and
load it in your suite with `Configure Platform    windows    external=False`.

### Out-of-tree (external) platform packages

You don't have to add your platform inside the `zaero` package at all.
Ship it as its own installable Python package (e.g. `zaero-rdkbmeshzap`)
that exposes a top-level module + class named exactly like the platform
string, e.g.:

```python
# rdkbmeshzap/__init__.py  (a separately pip-installed package)
class rdkbmeshzap(FeatureClient, FeatureRadio, ...):
    ...
```

then load it with the default `external=True`:

```robotframework
Configure Platform    rdkbmeshzap
```

which resolves to `importlib.import_module("rdkbmeshzap")` instead of
`zaero.rdkbmeshzap`. This is how vendor/OEM-specific device support (e.g.
RDK-B mesh nodes) can live in its own repository without ever touching the
core `zaero` package.

## Writing a new keyword (map) module

Keyword modules live in `zaero/map/` and are the only thing test suites
call directly. A minimal module looks like:

```python
# zaero/map/example.py
from robot.api.deco import keyword
from zaero.bridge.database_module import DatabaseModule
from zaero.bridge.platform_modules import PlatformModules
import zaero.utils.zi_logger as zi_logger


class Example(DatabaseModule, PlatformModules):
    """Keywords for <feature>."""

    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self):
        DatabaseModule.__init__(self)
        PlatformModules.__init__(self)
        self.db_obj = self.get_database_module_object()

    @keyword("Do Something")
    def do_something(self, device: str, value: str):
        """
        One-line summary.

        - ``device`` is the name given to the device in the config file
        - ``value`` ...

        Example:
        | Do Something | ap | foo |
        """
        platform = self.db_obj.read_from_database(device, 'platform')
        platform_obj = self.get_platform_module_object(platform)
        return platform_obj.do_something(device, value)
```

Then add `Example` to the `zaero` class in `zaero/__init__.py`, both in the
base-class list and the `__init__` chain:

```python
from zaero.map.example import Example

class zaero(Client, Connection, Database, Ping, Ui,
            PacketSniffer, PacketCapture, platform, PduControl,
            Example):
    def __init__(self):
        ...
        Example.__init__(self)
```

**Guidelines** (matching the style of the existing `zaero/map/*.py`
modules):

- Keep `ROBOT_AUTO_KEYWORDS = False` and decorate only the methods meant to
  be Robot Framework keywords with `@keyword("Title Case Name")`.
- A keyword should read `platform`/`connection` from the database and
  delegate — it should not contain platform-specific logic itself. That
  logic belongs in a platform plugin (`zaero/<platform>/feature_*.py`) or a
  utils driver (`zaero/utils/*.py`).
- Follow the existing docstring convention (`` `` `arg` `` description
  lines + an `Example:` table) — it's what test authors read to learn the
  keyword.

## Writing a new connection transport

Connection drivers implement `connect_with_device`, `execute_command`,
`close_connection`, `is_device_alive`, `get_file` and `put_file`, each
taking the `device` name as its first argument (see `SshInterface` in `zaero/utils/ssh_interface.py` for the
full pattern, including multi-hop tunnelling). Register the new class in
`zaero/bridge/connection_modules.py`:

```python
from zaero.utils.telnet_interface import TelnetInterface

class ConnectionModules:
    __modules = {
        'ssh': SshInterface,
        'adb': AdbInterface,
        'serial': SerialInterface,
        'telnet': TelnetInterface,   # new
    }
```

Devices can then set `connection: 'telnet'` in the testbed database, and
`Connect With Device` / `Execute Command` / ... will dispatch to it
automatically.

## Writing a new utils module

Utilities that aren't per-platform (packet capture/sniffing, PDU control,
protocol analysers) are registered the same way, in
`zaero/bridge/utils_modules.py`:

```python
from zaero.utils.new_tool import NewTool

class UtilsModules:
    __modules = {
        'sniffer': PacketSniffer,
        'capture': PacketCapture,
        'pdu': PduController,
        'new_tool': NewTool,          # new
    }
```

Then expose it through a `zaero/map/*.py` keyword module using
`self.get_utils_module_object('new_tool')`, following the pattern in
`zaero/map/pdu.py`.

## Adding a new template (base ABC)

If a new feature area doesn't fit any existing `base_feature_*.py`, add a
new ABC under `zaero/base/`, following the existing style:

```python
# zaero/base/base_feature_new_area.py
from abc import ABC, abstractmethod


class BaseFeatureNewArea(ABC):
    """Abstract class for the APIs in <new area>."""

    @abstractmethod
    def do_the_thing(self, device: str):
        raise NotImplementedError("Subclass must implement do_the_thing()")
```

Platform plugins that support the new area implement it alongside their
existing bases (e.g. `class FeatureClient(BaseFeatureClient,
BaseFeatureNewArea, ...)`), and a new `zaero/map/*.py` module exposes the
corresponding keywords, exactly as described above.
