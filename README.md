# DICOM Echo

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A lightweight, cross-platform, blazingly fast implementation of the `C-ECHO`\[^1\] DICOM procedure. 🔥

This package implements a service class user (SCU)\[^2\] app which functions like a `ping`, testing that the peer service class provider (SCP)\[^2\] is accepting associations for the given AE titles\[^3\].

Both a simple CLI and a Python API are provided for easy integration with your DICOM projects.

## Installation

[`pipx`](https://github.com/pypa/pipx) is recommended to install `dicom-echo` as a standalone CLI utility:

```sh
pipx install dicom-echo

# or if integrating with another Python project:
pip3 install dicom-echo
```

## CLI Usage

To send a `C-ECHO` request to `localhost:11111`:

```sh
❯ dicom-echo localhost:11111
✅ Success

❯ dicom-echo --help
```

```
 Usage: dicom-echo [OPTIONS] HOST

 Send a `C-ECHO` request to the given address.
 The `C-ECHO` procedure functions like a `ping`, serving to test that the peer SCP is accepting associations.

 This command will fail if the peer SCP is unreachable or rejects the association request for the given AE titles.

 Reference: https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5

╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    host      TEXT  The socket address of the peer SCP: {host}:{port}                  [required]                │
│                      Optionally, the AE title may be included: {AE title}@{host}:{port}                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -V        display the version of this program                                               │
│ --install-completion            Install completion for the current shell.                                         │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.  │
│ --help                -h        Show this message and exit.                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ DICOM Options ───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --called,--called-ae-title    -aec      TEXT     peer AE title of the host SCP [default: ANY-SCP]                 │
│ --calling,--calling-ae-title  -aet      TEXT     the AE title of this client [default: ECHOSCU]                   │
│ --id,--message-id             -id       INTEGER  the message ID to send [default: 1]                              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## API Usage

The `dicom_echo` module provides a simple API for sending `C-ECHO` requests:

```python
>>> import dicom_echo as echo

>>> echo.send('localhost:11111')
0
```

See the [API documentation](https://dicom-echo.readthedocs.io/en/latest/) for more details.

\[^1\]: for additional details, see [9.3.5 `C-ECHO` protocol | DICOM PS3.7 2024c - Message Exchange](https://dicom.nema.org/medical/dicom/current/output/chtml/part07/sect_9.3.5.html#sect_9.3.5.1)
\[^2\]:
[6.7 Service Class Specification | DICOM PS3.4 2024c - Service Class Specifications](https://dicom.nema.org/medical/dicom/current/output/chtml/part04/sect_6.7.html#:~:text=The%20SCU%20or%20user%20agent,are%20determined%20during%20Association%20establishment.) for the definitions of service class user (SCU) and service class provider (SCP):

```
> The SCU or user agent acts as the 'client,' while the SCP or origin server acts as the 'server'. For DIMSE based services the SCU/SCP roles are determined during Association establishment
```

\[^3\]:
[C.1: DICOM Application Entity Titles | DICOM PS3.8 2024c - Network Communication Support for Message Exchange](https://dicom.nema.org/medical/dicom/current/output/chtml/part08/chapter_C.html):

```
> A DICOM Application Entity Title uniquely identifies a service or application on a specific system in the network.
```
