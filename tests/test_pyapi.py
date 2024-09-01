"""Test the API exposed by this package."""

from __future__ import annotations

import shutil
import subprocess
from typing import TYPE_CHECKING
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


@depends_on_dicom_storescp
def test_dicom_storescp_version() -> None:
    """Test the version of the `dicom-storescp` command."""
    _, raw_version = subprocess.check_output([dicom_storescp, '--version']).decode('utf-8').strip().split()
    version = Version.parse(raw_version)

    assert version >= Version(0, 7, 0)


@mock.patch('dicom_echo.__send')
def test_message_id_counter(mock_backend_send: MagicMock) -> None:
    """Verify that the message ID counter increments on each call to `dicom_echo.send()`."""
    # Arrange
    num_calls = 4

    # Act
    for _ in range(num_calls):
        echo.send('dummy')

    # Assert
    assert mock_backend_send.call_count == num_calls

    message_ids = [call.args[-1] for call in mock_backend_send.call_args_list]
    assert message_ids == list(range(1, num_calls + 1))
