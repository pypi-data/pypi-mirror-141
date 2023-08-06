# Development

## Clone

```bash
$ git clone git@gitlab.com:cbjh/memgen/py-memgen.git
```

## Prerequisites

```bash
$ sudo apt-get install python3-venv
```

## Setup

```bash
$ cd py-memgen
$ python3 -m venv .venv
```

**Note**: Both VSCode and PyCharm integrate with `venv`, but they might not do this automatically.
Selection of Python interpreter/environment is accessible on the status bar for both editors. Reopen terminal afterwards.

To manually activate the environment 

```bash
$ . .venv/bin/activate
```

Installation of `memgen` in editable mode

```bash
(venv) $ pip install -e .
```

Files in `memgen` folder can be edited without need for re-installation.

Re-installation still needs to be done if the folder is moved

```bash
(venv) $ pip install -e .
```

## Test

```bash
memgen example/dmpc.pdb example/dopc.pdb membrane.pdb --ratio 20 80 --png membrane.png --server localhost:3000
```

You can use VSCode test panel, to run unit tests. Framework: `pytest`, location: `src/memgen`.

## Install (alternative)

`pip` can be used, to install a branch directly from GitLab

```bash
$ pip3 install git+https://gitlab.com/cbjh/memgen/py-memgen.git@main
```

Such installation is read-only, so it is not useful for development, but it might be useful for testing.

# Packaging

```bash
$ . .venv/bin/activate
(venv) $ pip install --upgrade pip setuptools wheel build twine
```

# Publishing

- Create a tag in GitLab
- Start the last (manual) job in the pipeline
