"""Test the API exposed by this package."""

from __future__ import annotations

import shutil
import socket
import subprocess
from typing import TYPE_CHECKING, Iterator
from unittest import mock

import pytest
from semver import Version

import dicom_echo as echo

if TYPE_CHECKING:  # pragma: no cover
    from unittest.mock import MagicMock

    dicom_storescp = 'dicom-storescp'
else:
    dicom_storescp = shutil.which('dicom-storescp')

depends_on_dicom_storescp = pytest.mark.skipif(
    not dicom_storescp, reason='`dicom-storescp` not found. To install it, run `cargo install dicom-storescp`'
)

dummy_address = 'dummy:1234'


@pytest.fixture(scope='session')
def localhost() -> Iterator[tuple[str, int]]:
    """Query the OS for the first available port; return the hostname of the socket as well."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', 0))
        host, port = sock.getsockname()
        sock.close()
        yield (host, port)


@pytest.fixture(scope='session')
def scpserver(localhost: tuple[str, int]) -> Iterator[tuple[subprocess.Popen[str], str]]:
    """Start a DICOM SCP server for use in tests."""
    host, port = localhost
    with subprocess.Popen([dicom_storescp, '-p', str(port)], text=True) as sub_proc:
        with pytest.raises(subprocess.TimeoutExpired):
            sub_proc.wait(timeout=0.01)

        assert None is sub_proc.returncode

        try:
            yield (sub_proc, f'{host}:{port}')
        finally:
            sub_proc.terminate()


@depends_on_dicom_storescp
def test_dicom_storescp_version() -> None:
    """Test the version of the `dicom-storescp` command."""
    _, raw_version = subprocess.check_output([dicom_storescp, '--version']).decode('utf-8').strip().split()
    version = Version.parse(raw_version)

    assert Version(0, 7, 0) <= version


@depends_on_dicom_storescp
def test_send_echo(scpserver: tuple[subprocess.Popen[str], str]) -> None:
    """Test sending a C-ECHO message to a local DICOM SCP server."""
    # Arrange
    _, address = scpserver

    # Act
    rc = echo.send(address)

    # Assert
    assert 0 == rc


@mock.patch('dicom_echo.__send')
@mock.patch('dicom_echo.counter', new_callable=echo.Counter)
def test_message_id_counter(mock_counter: echo.Counter, mock_backend_send: MagicMock) -> None:
    """Verify that the message ID counter increments on each call to `dicom_echo.send()`."""
    # Arrange
    num_calls = 4

    # Act
    for _ in range(num_calls):
        echo.send(dummy_address)

    # Assert
    assert num_calls == mock_backend_send.call_count
    assert num_calls == mock_counter.count

    message_ids = [call.kwargs['message_id'] for call in mock_backend_send.call_args_list]
    assert list(range(1, num_calls + 1)) == message_ids


@mock.patch('dicom_echo.__send')
@mock.patch('dicom_echo.counter', new_callable=echo.Counter)
def test_default_values(mock_counter: echo.Counter, mock_backend_send: MagicMock) -> None:
    """Verify that the message ID counter increments on each call to `dicom_echo.send()`."""
    echo.send(dummy_address)

    mock_backend_send.assert_called_once()
    assert dummy_address == mock_backend_send.call_args.args[0]
    assert echo.DEFAULT_CALLED_AE_TITLE == mock_backend_send.call_args.kwargs['called_ae_title']
    assert echo.DEFAULT_CALLING_AE_TITLE == mock_backend_send.call_args.kwargs['calling_ae_title']
    assert mock_counter.count == mock_backend_send.call_args.kwargs['message_id']


@mock.patch('dicom_echo.__send')
def test_message_id_override(mock_backend_send: MagicMock) -> None:
    """Verify that the default count-based message ID can be overridden."""
    # Arrange
    message_id = 42

    # Act
    echo.send(dummy_address, message_id=message_id)

    # Assert
    mock_backend_send.assert_called_once()
    assert message_id == mock_backend_send.call_args.kwargs['message_id']
