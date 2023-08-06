import os
from typing import Any
import yaml
import idac_sdk
from idac_sdk.models.config import iDACConfig


DIR_PATH = os.path.dirname(idac_sdk.__file__)
IDAC_CONFIG_FOLDER = os.path.join(DIR_PATH, ".idac")
IDAC_CONFIG_FILE = os.path.join(IDAC_CONFIG_FOLDER, "config")
EMPTY_CONFIG: Any = {
    "defaults": {
        "idac_fqdn": "",
        "idac_proto": "https",
        "auth_type": idac_sdk.IDACAuthType.DCLOUD_SESSION.name,
        "auth": "",
        "api_version": "2.0",
    }
}


def have_config() -> bool:
    """Checks if config file exists

    Returns:
        bool: True if exists
    """
    return os.path.exists(IDAC_CONFIG_FILE)


def load_config() -> iDACConfig:
    """Loads either existing or empty iDAC config

    Returns:
        iDACConfig: loaded config
    """
    if not os.path.exists(IDAC_CONFIG_FOLDER):
        os.mkdir(IDAC_CONFIG_FOLDER)

    if os.path.exists(IDAC_CONFIG_FILE):
        with open(IDAC_CONFIG_FILE, "r") as file:
            current_config = yaml.safe_load(file)
        return iDACConfig(**current_config)
    else:
        return iDACConfig(**EMPTY_CONFIG)
