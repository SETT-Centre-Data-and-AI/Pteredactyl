from typing import Any, NoReturn

from pteredactyl.mappings import configuration


def _get_config(model_path: str) -> dict[str, Any] | NoReturn:
    config = configuration.get(model_path)

    if config:
        return config

    else:
        available_list = [k for k in configuration.keys()]
        available = "\n -> " + (
            "\n -> ".join(available_list) if available_list else "None"
        )
        raise ValueError(
            f"Could not find config for '{model_path}' (please check pteredactyl.mappings). Available models: {available}"
        )
