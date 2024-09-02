"""Configure tests and define test fixtures."""

from __future__ import annotations

import socket
import subprocess
from typing import TYPE_CHECKING, Iterator

import pytest

if TYPE_CHECKING:  # pragma: no cover
    from unittest.mock import MagicMock

    from pytest_mock import MockerFixture


@pytest.fixture(scope='session')
def dicom_storescp() -> str:
    """Return the path to the `dicom-storescp` executable."""
    import shutil

    if (dicom_storescp := shutil.which('dicom-storescp')) is None:
        pytest.skip('`dicom-storescp` not found. To install it, run `cargo install dicom-storescp`')

    return dicom_storescp


@pytest.fixture(scope='session')
def localhost() -> Iterator[tuple[str, int]]:
    """Query the OS for the first available port; return the hostname of the socket as well."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', 0))
        host, port = sock.getsockname()
        sock.close()
        yield (host, port)


@pytest.fixture(scope='session')
def scpserver(dicom_storescp: str, localhost: tuple[str, int]) -> Iterator[str]:
    """Start a DICOM SCP server for use with tests."""
    host, port = localhost
    with subprocess.Popen([dicom_storescp, '-p', str(port)], text=True) as sub_proc:
        with pytest.raises(subprocess.TimeoutExpired):
            sub_proc.wait(timeout=0.01)

        assert None is sub_proc.returncode

        try:
            yield f'{host}:{port}'
        finally:
            sub_proc.terminate()


@pytest.fixture
def mock_send_rc0(mocker: MockerFixture) -> MagicMock:
    """Mock the `dicom_echo.__send` function with a return code of `0`."""
    return mocker.patch('dicom_echo.__send', return_value=0)


@pytest.fixture
def mock_send_rc1(mocker: MockerFixture) -> MagicMock:
    """Mock the `dicom_echo.__send` function with a return code of `1`."""
    return mocker.patch('dicom_echo.__send', return_value=1)
