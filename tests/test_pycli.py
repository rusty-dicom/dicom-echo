"""Test the CLI provided by `dicom_echo`."""

from __future__ import annotations

from typing import TYPE_CHECKING

import rich.emoji
from typer.testing import CliRunner

import dicom_echo as echo
from dicom_echo.cli import app, command

if TYPE_CHECKING:  # pragma: no cover
    from unittest.mock import MagicMock

runner = CliRunner()


def test_help() -> None:
    """Test the response of the `--help` flag."""
    result = runner.invoke(app, ['--help'])

    assert 0 == result.exit_code
    assert 'Usage' in result.stdout
    assert 'Arguments' in result.stdout
    assert 'Options' in result.stdout
    assert 'DICOM Options' in result.stdout


def test_success(scpserver: str) -> None:
    """Test the CLI output when the DICOM SCP server is accepting associations."""
    result = runner.invoke(app, [scpserver])

    assert 0 == result.exit_code
    assert '✅ Success\n' == result.stdout


def test_failure() -> None:
    """Test the CLI when the DICOM SCP server is unreachable."""
    result = runner.invoke(app, ['dummy:1234'])

    assert 1 == result.exit_code
    assert ConnectionError is result.exception.__class__


def test_version() -> None:
    """Test the CLI output when the `--version` flag is provided."""
    result = runner.invoke(app, ['--version'])

    assert 0 == result.exit_code
    assert command in result.stdout
    assert echo.__version__ in result.stdout


def test_version_called_as_module() -> None:
    """Test the CLI output when the utility is invoked as a Python module."""


def test_host_aetitle(mock_send_rc0: MagicMock) -> None:
    """Verify the called AE title may be passed with the target address."""
    # Arrange
    called_ae_title = 'dummy'

    # Act
    runner.invoke(app, [f'{called_ae_title}@localhost:1234'])

    # Assert
    mock_send_rc0.assert_called_once()
    assert mock_send_rc0.call_args.kwargs['called_ae_title'] == 'dummy'


def test_nonzero_response(mock_send_rc1: MagicMock) -> None:
    """Test the CLI output when the DICOM SCP returns a non-zero status code."""
    result = runner.invoke(app, ['dummy:1234'])

    assert mock_send_rc1.return_value == result.exit_code
    assert 'Warning:' in result.stdout
    assert rich.emoji.Emoji.replace(':warning:') in result.stdout
    assert str(mock_send_rc1.return_value) in result.stdout
