""".. include:: ../../README.md
  :start-line: 3

# Submodules

## `dicom_echo.backend`

This module is built with Rust and provides the core functionality for sending `C-ECHO` messages. See
[/backend/](./backend/index.html) for the crate's documentation.

## `dicom_echo.cli`

A simple CLI for sending `C-ECHO` messages. Built with `typer`.
"""  # noqa: D205, D415

from __future__ import annotations

import sys

if not sys.argv[0].endswith('pdoc'):
    from dicom_echo.backend import (  # pylint: disable=no-name-in-module
        DEFAULT_CALLED_AE_TITLE,
        DEFAULT_CALLING_AE_TITLE,
    )
    from dicom_echo.backend import send as __send  # pylint: disable=no-name-in-module
else:
    DEFAULT_CALLED_AE_TITLE = 'ANY-SCP'  # pyright: ignore[reportConstantRedefinition]
    DEFAULT_CALLING_AE_TITLE = 'ECHOSCU'  # pyright: ignore[reportConstantRedefinition]

    def __send(
        address: str,
        /,
        called_ae_title: str = DEFAULT_CALLED_AE_TITLE,
        calling_ae_title: str = DEFAULT_CALLING_AE_TITLE,
        message_id: int = 1,
    ) -> int:
        """Send a `C-ECHO` message to the given address.

        Reference: [DICOM Standard Part 7, Section 9.1.5](https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5)
        """
        return 0


__all__ = ['DEFAULT_CALLED_AE_TITLE', 'DEFAULT_CALLING_AE_TITLE', 'send']

__version__ = '0.0.0'
__version_tuple__ = (0, 0, 0)


class Counter:
    """A simple counter."""

    count = 0

    def increment(self) -> int:
        """Increment and return the counter."""
        self.count += 1
        return self.count


class Sentinel:
    """Explicitly define a class for the sentinel object for type annotations."""


counter = Counter()
sentinel = Sentinel()


def send(
    address: str,
    /,
    called_ae_title: str = DEFAULT_CALLED_AE_TITLE,
    calling_ae_title: str = DEFAULT_CALLING_AE_TITLE,
    message_id: int | Sentinel = sentinel,
) -> int:
    """Send a `C-ECHO` message to the given address.

    If `message_id` is not overwritten, a global counter will be incremented and passed.

    Reference: [DICOM Standard Part 7, Section 9.1.5](https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5)
    """
    if isinstance(message_id, Sentinel):
        message_id = counter.increment()
    return __send(address, called_ae_title=called_ae_title, calling_ae_title=calling_ae_title, message_id=message_id)
