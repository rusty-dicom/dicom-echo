""".. include:: ./cli.md"""  # noqa: D415

from __future__ import annotations

import logging
import sys
from pathlib import Path

import rich
import typer

import dicom_echo as echo

try:
    import typing as t

    _ = t.Annotated, t.TypeAlias  # type: ignore[attr-defined]
except AttributeError:  # pragma: no cover
    # note: for supporting Python 3.8
    import typing_extensions as t  # type: ignore[no-redef]

__all__ = ['main', 'version_callback']

logger = logging.getLogger(__name__)

app = typer.Typer(context_settings={'help_option_names': ['-h', '--help']}, rich_markup_mode='rich')
this = Path(sys.argv[0]).resolve()
command = this.name if this.name != '__main__.py' else this.parent.name


def version_callback(value: bool | None) -> None:
    """Print the version of this program."""
    if not value:
        return

    rich.print(f'[bold bright_black]{command}[/bold bright_black] {echo.__version__}')
    raise typer.Exit()


AEC: t.TypeAlias = t.Annotated[
    str,
    typer.Option(
        '-aec', '--called', '--called-ae-title', rich_help_panel='DICOM Options', help='peer AE title of the host SCP'
    ),
]

AET: t.TypeAlias = t.Annotated[
    str,
    typer.Option(
        '-aet', '--calling', '--calling-ae-title', rich_help_panel='DICOM Options', help='the AE title of this client'
    ),
]

ID: t.TypeAlias = t.Annotated[
    int, typer.Option('-id', '--id', '--message-id', rich_help_panel='DICOM Options', help='the message ID to send')
]

VER: t.TypeAlias = t.Annotated[
    bool,
    typer.Option(
        '-V',
        '--version',
        callback=version_callback,
        is_eager=True,
        help='display the version of this program',
    ),
]

BLUE_HOST_PURPLE_PORT = r'[blue]{host}[/blue]:[purple]{port}[/purple]'
GREEN_AET_BLUE_HOST_PURPLE_PORT = r'[green]{AE title}[/green]@' + BLUE_HOST_PURPLE_PORT
HOST_OPTION_HELP = f"""The socket address of the peer SCP: {BLUE_HOST_PURPLE_PORT}

    Optionally, the AE title may be included: {GREEN_AET_BLUE_HOST_PURPLE_PORT}
"""


@app.command()
def main(
    host: t.Annotated[str, typer.Argument(show_default=False, help=HOST_OPTION_HELP)],
    called_ae_title: AEC = echo.DEFAULT_CALLED_AE_TITLE,
    calling_ae_title: AET = echo.DEFAULT_CALLING_AE_TITLE,
    message_id: ID = 1,
    version: VER = False,
) -> None:
    """Send a `C-ECHO` request to the given address.

    The `C-ECHO` procedure functions like a `ping`, serving to test that the peer SCP is accepting associations.

    This command will fail if the peer SCP is unreachable or rejects the association request for the given AE titles.

    Reference: https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5
    """
    if '@' in host and called_ae_title == echo.DEFAULT_CALLED_AE_TITLE:
        called_ae_title, _ = host.split('@')

    if rc := echo.send(host, called_ae_title, calling_ae_title, message_id):
        rich.print(f':warning: [orange]Warning[/orange]: received non-zero status code: {rc}')
        raise typer.Exit(rc)

    rich.print(':white_check_mark: [green]Success[/green]')


logger.debug('successfully imported %s', __name__)
