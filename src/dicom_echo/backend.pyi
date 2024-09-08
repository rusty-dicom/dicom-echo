from typing import Literal

DEFAULT_CALLED_AE_TITLE: Literal['ANY-SCP'] = 'ANY-SCP'
"""By default, specify this AE title for the target SCP."""

DEFAULT_CALLING_AE_TITLE: Literal['ECHOSCU'] = 'ECHOSCU'
"""By default, specify this AE title for the SCU sending the `C-ECHO` message."""

def send(
    address: str,
    /,
    called_ae_title: str = DEFAULT_CALLED_AE_TITLE,
    calling_ae_title: str = DEFAULT_CALLING_AE_TITLE,
    message_id: int = 1,
) -> int:
    """Send a `C-ECHO` message to the given address.

    Reference: [DICOM Standard Part 7, Section 9.1.5](https://www.dicomstandard.org/standards/view/message-exchange#sect_9.1.5)
    """
