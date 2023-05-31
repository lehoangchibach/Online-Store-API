# Got It's Final Project Template

## Requirements

- Python 3.10+
- MySQL 5.7+
- [Poetry](https://python-poetry.org/)

## Installation

### Set up virtual environment

```shell
pip install virtualenv
virtualenv venv
source ./venv/bin/activate
```

### Install dependencies

```shell
poetry install
```

### Install `pre-commit` hooks

- Install `pre-commit`: https://pre-commit.com/ (should be installed globally)
- Install `pre-commit` hooks:

  ```shell
  pre-commit install
  ```

## Running

Inside the virtual environment, run

```shell
python run.py
```
