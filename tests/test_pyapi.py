"""Test the API exposed by this package."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING
from unittest import mock

from semver import Version

import dicom_echo as echo

if TYPE_CHECKING:  # pragma: no cover
    from unittest.mock import MagicMock

dummy_address = 'dummy:1234'


def test_dicom_storescp_version(dicom_storescp: str) -> None:
    """Test the version of the `dicom-storescp` command."""
    _, raw_version = subprocess.check_output([dicom_storescp, '--version'], text=True).split()
    version = Version.parse(raw_version)

    assert Version(0, 7, 0) <= version


def test_send_echo(scpserver: str) -> None:
    """Test sending a C-ECHO message to a local DICOM SCP server."""
    rc = echo.send(scpserver)

    assert 0 == rc


@mock.patch('dicom_echo.counter', new_callable=echo.Counter)
def test_message_id_counter(mock_counter: echo.Counter, mock_send_rc0: MagicMock) -> None:
    """Verify that the message ID counter increments on each call to `dicom_echo.send()`."""
    # Arrange
    num_calls = 4

    # Act
    for _ in range(num_calls):
        echo.send(dummy_address)

    # Assert
    assert num_calls == mock_send_rc0.call_count
    assert num_calls == mock_counter.count

    message_ids = [call.kwargs['message_id'] for call in mock_send_rc0.call_args_list]
    assert list(range(1, num_calls + 1)) == message_ids


@mock.patch('dicom_echo.counter', new_callable=echo.Counter)
def test_default_values(mock_counter: echo.Counter, mock_send_rc0: MagicMock) -> None:
    """Verify that the message ID counter increments on each call to `dicom_echo.send()`."""
    echo.send(dummy_address)

    mock_send_rc0.assert_called_once()
    assert dummy_address == mock_send_rc0.call_args.args[0]
    assert echo.DEFAULT_CALLED_AE_TITLE == mock_send_rc0.call_args.kwargs['called_ae_title']
    assert echo.DEFAULT_CALLING_AE_TITLE == mock_send_rc0.call_args.kwargs['calling_ae_title']
    assert mock_counter.count == mock_send_rc0.call_args.kwargs['message_id']


def test_message_id_override(mock_send_rc0: MagicMock) -> None:
    """Verify that the default count-based message ID can be overridden."""
    # Arrange
    message_id = 42

    # Act
    echo.send(dummy_address, message_id=message_id)

    # Assert
    mock_send_rc0.assert_called_once()
    assert message_id == mock_send_rc0.call_args.kwargs['message_id']
