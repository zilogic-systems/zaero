# ZAERO

## Description

**zaero** is a python-based test automation framework targetted to test networking devices like AP, Routers, Mesh Nodes and wireless clients.

---

## Prerequisites

Make sure you have the following installed:

* Python 3.8+
* pip (Python package manager)
* Linux environment (recommended)

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/zilogic-systems/zaero.git
```

### 2. Install zaero Package

```
cd zaero/packages/
python3 -m pip install zaero-1.0.0-py3-none-any.whl
```

### 3. Install Dependencies

```
cd ..
python3 -m pip install -r requirements.txt
```

### 4. Install Playwright

```
playwright install --with-deps
```

---

## Configuration

### Fields to Fill in `dut.yaml`

Before running the test suite, update the login credentials of the controller in `zaero/test/config/dut.yaml` with your environment-specific values.

### Update SSID Configuration in `test_ssid_config.py`

The file `dut.yaml` contains predefined SSIDs:

* mld_ssid_1
* mld_ssid_2
* mld_ssid_3

The SSID mentioned in the `test_config_ssid()` test case has to be changed to other SSID before executing the test.

Ex:

If the ssid mentioned is,

	ssid = initialize.read_from_database("controller", "mld_ssid_3")

It has to be changed to `"mld_ssid_2"` or `"mld_ssid_1"`

	ssid = initialize.read_from_database("controller", "mld_ssid_1")

---

## Usage

### Run Test Cases

```
cd zaero/test/
python3 -m pytest --log-cli-level=INFO test_ssid_config.py -v -s
```

---

## Author

Zilogic Systems