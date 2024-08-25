# Contributing to `dicom-echo`

Welcome! Thank you for considering to contribute to `dicom-echo`! Here are some guidelines to help you get started.

## Table of Contents

- [Contributing to `dicom-echo`](#contributing-to-dicom-echo)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [License](#license)

## Code of Conduct

Please observe our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for all contributors.

## Getting Started

The `dicom-echo` backend is written in Rust. You'll need to install the [Rust toolchain] for development.

You'll also need to install [`poetry`] (and a couple of plugins), [`pre-commit`] for managing git hooks and linting checks, and [`direnv`] for automating maintenance of your local development environment.

1. Set up [`poetry`] and [`pre-commit`] by running the following from the root of this repo:

   ```sh
   # install pipx, a utility to install python programs in isolated environments
   # note: pipx can also be installed with 'apt install pipx' or 'brew install pipx'
   pip3 install pipx && pipx ensurepath

   # install poetry for managing dependencies and virtual environments
   pipx install poetry

   # install pre-commit (it tends to work better when installed globally)
   pipx install pre-commit

   # install the 'poethepoet' plugin to enable custom poetry commands in 'pyproject.toml'
   poetry self add 'poethepoet[poetry_plugin]'

   # enable the poetry-dynamic-versioning plugin
   poetry setup-versioning
   ```

1. [Install `direnv`] and [hook it into your shell]:

   ```sh
   # install direnv, assuming your OS is Ubuntu ('brew install direnv' for macOS)
   sudo apt update && sudo apt install -y direnv

   # hook direnv into each shell session by updating your shell's rc file (assuming bash or zsh)
   printf 'command -v direnv >/dev/null 2>&1 &&\n  eval "$(direnv hook %s)"\n' "${SHELL##*/}" >> ~/.${SHELL##*/}rc

   # hook direnv into the current shell session (or restart your shell)
   eval "$(direnv hook "${SHELL##*/}")"
   ```

You can now run the following from the root of this repo to finish the setup:

```sh
# allow direnv to automatically execute the .envrc script each time you cd into the repo
direnv allow

# build and install this package in development mode with `maturin`
poetry install
```

We use [`poetry`], [`poetry-dynamic-versioning`], and [`poethepoet`] to manage dependencies, versioning, and tasks. Since we need to compile Rust, we use [`maturin`] as the build system instead of the default [`poetry-core`]. Poetry's `package-mode` is disabled in [`pyproject.toml`] to allow for this, meaning that several core `poetry` commands will not work.

Instead, we use [poetry hooks] with [`poethepoet`] to replace the functionality of the disabled commands. Note that commands such as `poetry build` will return a non-zero exit code whether or not the build was successful. This is expected (for now).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE.md).

[hook it into your shell]: https://direnv.net/docs/hook.html
[install `direnv`]: https://direnv.net/docs/installation.html
[poetry hooks]: https://poethepoet.natn.io/poetry_plugin.html#hooking-into-poetry-commands
[rust toolchain]: https://www.rust-lang.org/tools/install
[`direnv`]: https://direnv.net/
[`maturin`]: https://www.maturin.rs/
[`poethepoet`]: https://poethepoet.natn.io/
[`poetry-core`]: https://github.com/python-poetry/poetry-core
[`poetry-dynamic-versioning`]: https://github.com/mtkennerly/poetry-dynamic-versioning
[`poetry`]: https://python-poetry.org/
[`pre-commit`]: https://pre-commit.com/
[`pyproject.toml`]: pyproject.toml
