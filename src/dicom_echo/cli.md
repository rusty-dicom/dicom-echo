# `dicom-echo`

Send a `C-ECHO` message to the given address.

The `C-ECHO` procedure functions like a `ping`, serving to test that the peer SCP is accepting associations.

This command will fail if the peer SCP is unreachable or rejects the association request for the given AE titles.

Reference: https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5

## Usage

```console
$ dicom-echo [OPTIONS] HOST
```

## Arguments

- `HOST` \[required\]: The socket address of the peer SCP: <span style="color:blue">{host}</span>:<span style="color:purple">{port}</span>

  Optionally, the AE title may be included: <span style="color:green">{AE title}</span>@<span style="color:blue">{host}</span>:<span style="color:purple">{port}</span>

## Options

- `-aec, --called, --called-ae-title TEXT`: peer AE title of the host SCP \[default: `ANY-SCP`\]
- `-aet, --calling, --calling-ae-title TEXT`: the AE title of this client \[default: `ECHOSCU`\]
- `-id, --id, --message-id INTEGER`: the message ID to send \[default: `1`\]
- `-V, --version`: display the version of this program
- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.
