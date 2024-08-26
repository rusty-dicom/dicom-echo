class Request:
    """Send `C-ECHO` requests to a DICOM service class provider."""

    address: str
    called_ae_title: str
    calling_ae_title: str
    message_id: int

    def __init__(
        self, address: str, /, called_ae_title: str = 'ANY-SCP', calling_ae_title: str = 'ECHOSCU', message_id: int = 1
    ) -> None: ...
    def send(self) -> int:
        """Send the `C-ECHO` request and return the response's status."""

def do_sum(a: int, b: int) -> str:
    """Sum two numbers and return the result as a string.

    TODO: replace this dummy function when the real backend has been implemented.
    """
