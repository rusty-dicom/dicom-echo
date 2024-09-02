"""Define `pytest` fixtures for use throughout the `tests` package and `doctest` tests."""

from __future__ import annotations

import socket
import subprocess
from typing import Iterator

import pytest


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
