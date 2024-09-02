"""Configure tests and define test fixtures."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:  # pragma: no cover
    from unittest.mock import MagicMock

    from pytest_mock import MockerFixture


@pytest.fixture
def mock_send_rc0(mocker: MockerFixture) -> MagicMock:
    """Mock the `dicom_echo.__send` function with a return code of `0`."""
    return mocker.patch('dicom_echo.__send', return_value=0)


@pytest.fixture
def mock_send_rc1(mocker: MockerFixture) -> MagicMock:
    """Mock the `dicom_echo.__send` function with a return code of `1`."""
    return mocker.patch('dicom_echo.__send', return_value=1)
