"""Define a CLI ."""

from __future__ import annotations

import logging
from ctypes import c_uint32
from typing import Annotated

import typer
from rich import print

from echoscu import backend

logger = logging.getLogger(__name__)


def parse_uint(value: str) -> int:
    """Parse a string into an unsigned integer."""
    return c_uint32(int(value)).value


def main(
    a: Annotated[int, typer.Argument(parser=parse_uint, show_default=False, metavar='(uint32_t)')],
    b: Annotated[int, typer.Argument(parser=parse_uint, show_default=False, metavar='(uint32_t)')],
) -> None:
    """Print the sum of the given unsigned integers."""
    print(backend.do_sum(a, b))


logger.debug('successfully imported %s', __name__)
