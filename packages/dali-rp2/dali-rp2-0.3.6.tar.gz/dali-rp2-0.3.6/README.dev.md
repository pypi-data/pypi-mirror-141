<!--- Copyright 2022 eprbell --->

<!--- Licensed under the Apache License, Version 2.0 (the "License"); --->
<!--- you may not use this file except in compliance with the License. --->
<!--- You may obtain a copy of the License at --->

<!---     http://www.apache.org/licenses/LICENSE-2.0 --->

<!--- Unless required by applicable law or agreed to in writing, software --->
<!--- distributed under the License is distributed on an "AS IS" BASIS, --->
<!--- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. --->
<!--- See the License for the specific language governing permissions and --->
<!--- limitations under the License. --->

# DaLI for RP2 v0.3.6 Developer Guide
[![Static Analysis / Main Branch](https://github.com/eprbell/dali-rp2/actions/workflows/static_analysis.yml/badge.svg)](https://github.com/eprbell/dali-rp2/actions/workflows/static_analysis.yml)
[![Documentation Check / Main Branch](https://github.com/eprbell/dali-rp2/actions/workflows/documentation_check.yml/badge.svg)](https://github.com/eprbell/dali-rp2/actions/workflows/documentation_check.yml)
[![Unix Unit Tests / Main Branch](https://github.com/eprbell/dali-rp2/actions/workflows/unix_unit_tests.yml/badge.svg)](https://github.com/eprbell/dali-rp2/actions/workflows/unix_unit_tests.yml)
[![Windows Unit Tests / Main Branch](https://github.com/eprbell/dali-rp2/actions/workflows/windows_unit_tests.yml/badge.svg)](https://github.com/eprbell/dali-rp2/actions/workflows/windows_unit_tests.yml)
[![CodeQL/Main Branch](https://github.com/eprbell/dali-rp2/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/eprbell/dali-rp2/actions/workflows/codeql-analysis.yml)

## Table of Contents
* **[Introduction](#introduction)**
* **[License](#license)**
* **[Download](#download)**
* **[Setup](#setup)**
  * [Ubuntu Linux](#setup-on-ubuntu-linux)
  * [macOS](#setup-on-macos)
  * [Windows 10](#setup-on-windows-10)
  * [Other Unix-like Systems](#setup-on-other-unix-like-systems)
* **[Source Code](#source-code)**
* **[Development](#development)**
  * [Design Guidelines](#design-guidelines)
  * [Development Workflow](#development-workflow)
  * [Unit Tests](#unit-tests)
* **[DaLI Internals](#dali-internals)**
  * [Plugin Development](#plugin-development)
* **[Frequently Asked Developer Questions](#frequently-asked-developer-questions)**

## Introduction
This document describes [DaLI](https://github.com/eprbell/dali-rp2) setup instructions, development workflow, design principles, source tree structure and plugin architecture.

## License
DaLI is released under the terms of Apache License Version 2.0. For more information see [LICENSE](LICENSE) or <http://www.apache.org/licenses/LICENSE-2.0>.

## Download
The latest DaLI source can be downloaded at: <https://github.com/eprbell/dali-rp2>

## Setup
DaLI has been tested on Ubuntu Linux, macOS and Windows 10 but it should work on all systems that have Python version 3.7.0 or greater. Virtualenv is recommended for DaLI development. Note that requirements.txt contains `-e .`, which installs the DaLI package in editable mode.

### Setup on Ubuntu Linux
First make sure Python, pip and virtualenv are installed. If not, open a terminal window and enter the following commands:
```
sudo apt-get update
sudo apt-get install python3 python3-pip virtualenv
```

Then install DaLI Python package requirements:
```
cd <rp2_directory>
virtualenv -p python3 .venv
. .venv/bin/activate
.venv/bin/pip3 install -r requirements.txt
```
### Setup on macOS
First make sure [Homebrew](https://brew.sh) is installed, then open a terminal window and enter the following commands:
```
brew update
brew install python3 virtualenv
```

Then install DaLI Python package requirements:
```
cd <rp2_directory>
virtualenv -p python3 .venv
. .venv/bin/activate
.venv/bin/pip3 install -r requirements.txt
```
### Setup on Windows 10
First make sure [Python](https://python.org) 3.7 or greater is installed (in the Python installer window be sure to click on "Add Python to PATH"), then open a PowerShell window and enter the following commands:
```
python -m pip install virtualenv
```

Then install DaLI Python package requirements:
```
cd <rp2_directory>
virtualenv -p python .venv
.venv\Scripts\activate.ps1
python -m pip install -r requirements.txt
```
### Setup on Other Unix-like Systems
* install python 3.7 or greater
* install pip3
* install virtualenv
* cd _<dali_directory>_
* `virtualenv -p python3 .venv`
* `.venv/bin/pip3 install -r requirements.txt`

## Source Code
The RP2 source tree is organized as follows:
* `.bumpversion.cfg`: bumpversion configuration;
* `CHANGELOG.md`: change log document;
* `config/`: config files for examples and tests;
* `CONTRIBUTING.md`: contribution guidelines;
* `docs/`: additional documentation, referenced from the README files;
* `.editorconfig`;
* `.github/workflows/`: configuration of Github continuous integration;
* `.gitignore`;
* `input/`: examples and tests;
* `input/golden/`: expected outputs that Dali tests compare against;
* `.isort.cfg`: isort configuration;
* `LICENSE`: license information;
* `Makefile`: alternative old-school build flow;
* `MANIFEST.in`: source distribution configuration;
* `mypy.ini`: mypy configuration;
* `.pre-commit-config.yaml`: pre-commit configuration;
* `.pylintrc`: pylint configuration;
* `pyproject.toml`: packaging configuration;
* `README.dev.md`: developer documentation;
* `README.md`: user documentation;
* `requirements.txt`: Python dependency file for development;
* `setup.cfg`: static packaging configuration file;
* `setup.py`: dynamic packaging configuration file;
* `src/dali`: DaLI code, including classes for transactions, ODS and config genator, transaction resolver, etc.;
* `src/dali/data/`: spreadsheet templates that are used by the ODS generator;
* `src/dali/plugin/input/csv/`: CSV-based data loader plugins;
* `src/dali/plugin/input/rest/`: REST-based data loader plugins;
* `src/stubs/`: RP2 relies on the pyexcel-ezodf library, which doesn't have typing information, so it is added here;
* `tests/`: unit tests.

## Development
Read the [Contributing](CONTRIBUTING.md) document on pull requests guidelines.

### Design Guidelines
DaLI code adheres to these principles:
* immutability: generally data structures are read-only (the only exceptions are for data structures that would incur a major complexity increase without write permission: e.g. AVL tree node).
  * class fields are private (prepended with double-underscore). Fields that need public access have a read-only property. Write-properties are not used;
  * @dataclass classes have `frozen=True`
* runtime checks: parameters of public functions are type-checked at runtime
* type hints: all variables and functions have Python type hints;
* no id-based hashing: classes that are added to dictionaries and sets redefine `__eq__()`, `__neq__()` and `__hash__()`;
* encapsulated math: all high-precision math is done via `RP2Decimal` (a subclass of Decimal), to ensure the correct precision is used throughout the code. `RP2Decimal` instances are never mixed with other types in expressions;
* f-strings only: every time string interpolation is needed, f-strings are used;
* logging: logging is done via `logger.LOGGER`;
* no unnamed tuples: dataclasses or named tuples are used instead;
* one class per file (with exceptions for trivial classes);
* files containing a class must have the same name as the class (but lowercase with underscores): e.g. class AbstractEntry lives in file abstract_entry.py;
* abstract classes' name starts with `Abstract`
* no imports with `*`.

### Development Workflow
DaLI uses pre-commit hooks for quick validation at commit time and continuous integration via Github actions for deeper testing. Pre-commit hooks invoke: flake8, black, isort, pyupgrade and more. Github actions invoke: mypy, pylint, bandit, unit tests (on Linux, Mac and Windows), markdown link check and more.

While every commit and push are automatically tested as described, sometimes it's useful to run some of the above commands locally without waiting for continuous integration. Here's how to run the most common ones:
* run unit tests: `pytest --tb=native --verbose`
* type check: `mypy src tests`
* lint: `pylint -r y src tests/*.py`
* security check: `bandit -r src`
* reformat code: `black src tests`
* sort imports: `isort .`
* run pre-commit tests without committing: `pre-commit run --all-files`

Logs are stored in the `log` directory. To generate debug logs, prepend the command line with `LOG_LEVEL=DEBUG`, e.g.:
```
LOG_LEVEL=DEBUG bin/dali -s -o output/ config/test.ini
```

### Unit Tests
Unit tests are in the [tests](tests) directory. Please add unit tests for any new code.

## DaLI Internals
DaLI top-level function is in [dali_main.py](src/dali/dali_main.py). It performs the following operations:
* it reads the INI configuration file which includes data loader plugin initialization parameters;
* it instantiates data loader plugins using the initialization parameters from the config file and calls their load() method, which reads data from the source (CSV file or REST service) and returns it in a normalized format: a list of [AbstractTransaction](src/dali/abstract_transaction.py) instances, which can be any of its subclasses [InTransaction](src/dali/in_transaction.py) (acquired crypto), [OutTransaction](src/dali/out_transaction.py) (disposed-of crypto) or [IntraTransaction](src/dali/intra_transaction.py) (crypto transfer across accounts controlled by the same person);
* it passes the results of all plugin load() calls to the [transaction resolver](src/dali/transaction_resolver.py), which has the purpose of merging incomplete transactions, filling in any missing information (e.g. the spot price) and returning a normalized list of transactions (see below for more details);
* it passes the resolved data to the RP2 [ODS input file generator](src/dali/ods_generator.py) and to the RP2 [config file generator](src/dali/config_generator.py), which create the files to feed to RP2;

The transaction resolver is a critical component of DaLI and needs more description. Data loader plugins operate on incomplete information: e.g. if a transaction transfers crypto from Coinbase to Trezor, the Coinbase data loader plugin has no way of knowing that the destination address represents a Trezor account (because Coinbase itself doesn't have this information): so the plugin cannot fill the to_exchange and to_holder fields of the IntraTransaction (it fills them with `Keywords.UNKNOWN`). Similarly the Trezor data loader plugin cannot know that the source address belongs to a Coinbase account and therefore it cannot fill the from_exchange and from_holder fields of the IntraTransaction. So how does DaLI merge these two incomplete transactions into one complete IntraTransaction? It uses the transaction resolver, which relies on the `unique_id` field of each incomplete transaction: typically this is the transaction hash, but it could be an exchange-specific value that identifies uniquely the transaction. The transaction resolver analyzes all generated transactions, looks for incomplete ones with the same `unique_id` and merges them into a single one.

For this reason it's essential that all data loader plugins populate the `unique_id` field as best they can: without it the transaction resolver cannot merge incomplete data. Sometimes (especially with CSV files) hash information is missing and so it's impossible to populate the `unique_id` field: is such cases it's still possible to write a plugin, but the user will have to manually modify the generated result and perform transaction resolution manually, which is not ideal.

### Plugin Development
All data loader plugins are subclasses of [AbstractInputPlugin](src/dali/abstract_input_plugin.py) and they must:
* invoke the superclass constructor in their own constructor
* implement the load() method, which reads data from the native source and returns a list of AbstractTransaction instances, which can be InTransaction (acquired crypto), OutTransaction (disposed-of crypto) or IntraTransaction (crypto transfer across accounts controlled by the same person)

Data loader plugins live in one of the following directories, depending on their type (CSV or REST):
* `src/dali/plugin/input/csv/`;
* `src/dali/plugin/input/rest/`.

If a field is unknown fill it with `Keywords.UNKNOWN`, unless it's optional, in which case it can be left blank.

For an example of CSV-based data loader look at the [Trezor](src/dali/plugin/input/csv/trezor.py) plugin, for an example of REST-based data loader look at the [Coinbase](src/dali/plugin/input/rest/coinbase.py) plugin.

Here's a laundry list to use when submitting a new data loader plugin with a [PR](CONTRIBUTING.md#contributing-to-the-repository):
* ensure transactions have unique_id populated (typically with the hash), unless the information is missing from the native source: this is critical for the transaction resolver;
* ensure CSV data loaders have a comment at the beginning of the file, documenting the format. E.g.:
    ```
    # CSV Format: timestamp; type; transaction_id; address; fee; total
    ```
* ensure REST data loaders have three comments at the beginning of the file, containing links to:
  * REST API documentation
  * authentication procedure documentation
  * URL of the REST endpoint

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For example:
```
    # REST API: https://developers.coinbase.com/api/v2
    # Authentication: https://developers.coinbase.com/docs/wallet/api-key-authentication
    # Endpoint: https://api.coinbase.com
```
* ensure the __init__ method is calling the superclass constructor:
    ```
    super().__init__(account_holder)
    ```
* in the constructor create a plugin-specific logger with a name that uniquely identifies the specific instance of the plugin: this way in the logs it's easy to distinguish lines by plugin instance. Example of a plugin-specific log in the constructor of the Coinbase plugin:
    ```
    self.__logger: logging.Logger = create_logger(f"{self.__COINBASE}/{self.account_holder}")
    ```
* ensure self.__logger.debug() calls capture all of the native format data (this will occur only if the user sets `LOG_LEVEL=DEBUG` and it will be useful for debugging).

## Frequently Asked Developer Questions
Read the [frequently asked developer questions](docs/developer_faq.md).

