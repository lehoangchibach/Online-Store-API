import os.path
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config.base import BaseConfig

environment = os.getenv("ENVIRONMENT", "local")
if environment not in ["local", "test"]:
    config_file = f"config/{environment}.py"
    if not os.path.isfile(config_file):
        environment = "local"

config_name = f"config.{environment}"

module = import_module(config_name)

config: "BaseConfig" = module.Config
config.ENVIRONMENT = environment
