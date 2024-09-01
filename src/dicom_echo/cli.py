"""Define a CLI ."""

from __future__ import annotations

import logging
from typing import Annotated

import rich
import typer

import dicom_echo as echo

logger = logging.getLogger(__name__)

app = typer.Typer(context_settings={'help_option_names': ['-h', '--help']}, rich_markup_mode='rich')

_host_port = r'[blue]{host}[/blue]:[purple]{port}[/purple]'
_aet_host_port = r'[green]{AE title}[/green]@' + _host_port
_host_help = f"""The socket address of the peer SCP: {_host_port}

    Optionally, the AE title may be included: {_aet_host_port}
"""

AEC = Annotated[
    str,
    typer.Option(
        '-aec', '--called', '--called-ae-title', rich_help_panel='DICOM Options', help='peer AE title of the host SCP'
    ),
]

AET = Annotated[
    str,
    typer.Option(
        '-aet', '--calling', '--calling-ae-title', rich_help_panel='DICOM Options', help='the AE title of this client'
    ),
]


@app.command()
def main(
    host: Annotated[str, typer.Argument(show_default=False, help=_host_help)],
    called_ae_title: AEC = echo.DEFAULT_CALLED_AE_TITLE,
    calling_ae_title: AET = echo.DEFAULT_CALLING_AE_TITLE,
) -> None:
    """Send a `C-ECHO` message to the given address.

    The `C-ECHO` procedure functions like a `ping`, serving to test that the peer SCP is accepting associations.

    This command will fail if the peer SCP is unreachable or rejects the association request for the given AE titles.

    Reference: https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5
    """
    if '@' in host and called_ae_title == echo.DEFAULT_CALLED_AE_TITLE:
        called_ae_title, _ = host.split('@')

    if rc := echo.send(host, called_ae_title, calling_ae_title):
        rich.print(f':warning: [orange]Warning[/orange]: received non-zero status code: {rc}')
    else:
        rich.print(':white_check_mark: [green]Success[/green]')


logger.debug('successfully imported %s', __name__)
