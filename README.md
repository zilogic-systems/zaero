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

### 2. Generate .whl file

```
python3 -m pip install build
cd zaero/
python3 -m build
```

### 3. Install zaero Package

```
cd dist/
python3 -m pip install zaero-<version>py3-none-any.whl
```

### 4. Install Playwright

```
playwright install --with-deps
```

---



## Author

Zilogic Systems