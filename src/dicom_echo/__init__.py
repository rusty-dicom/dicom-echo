"""Define a CLI and an API for issuing DICOM's `C-ECHO` procedure."""

from __future__ import annotations

from dicom_echo.backend import DEFAULT_CALLED_AE_TITLE, DEFAULT_CALLING_AE_TITLE
from dicom_echo.backend import send as __send

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
    return __send(address, called_ae_title, calling_ae_title, message_id)
