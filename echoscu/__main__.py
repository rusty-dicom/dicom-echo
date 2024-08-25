"""The entrypoint for the `echoscu` CLI."""

import typer

from echoscu import cli


def main() -> None:
    """Execute the CLI's `main` function with `Typer`."""
    typer.run(cli.main)


if __name__ == '__main__':
    main()
