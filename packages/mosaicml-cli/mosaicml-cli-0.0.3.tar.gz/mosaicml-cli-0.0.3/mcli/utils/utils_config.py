"""Utils for modifying MCTL Configs"""
import json
import uuid
from typing import Any, Dict, Optional

import coolname
import fire
from jinja2 import Environment, StrictUndefined

from mcli.config import DEFAULT_CONFIG_PATH


def get_config_data() -> Dict[str, Any]:
    """Loads mctl config data

    Returns:
        Returns a dictionary with the mctl config data
    """
    try:
        with open(DEFAULT_CONFIG_PATH, 'r', encoding='utf8') as f:
            return json.load(f)
    except Exception as e:
        print('Unable to read the mctl config ~/.mosaic/config')
        raise Exception('Unable to read the mctl config ~/.mosaic/config') from e


def get_config_namespace() -> str:
    """Gets the default namespace for an mctl user

    Returns:
        Returns the default namespace
    """
    config_data = get_config_data()
    for _, data in config_data.items():
        if 'namespace' in data:
            # Returns first namespace found
            return data['namespace']
    raise Exception('Unable to find a default namespace for the user in the mctl config')


def get_unique_name(stem: Optional[str] = None):
    if stem is None:
        stem = coolname.generate_slug(2)
    return f'{stem}-{str(uuid.uuid4())[:6]}'


def format_jinja(input_text: str, config: dict):
    if input_text is None:
        return input_text

    env = Environment(undefined=StrictUndefined)
    template = env.from_string(input_text)
    return template.render(**config)


if __name__ == '__main__':
    fire.Fire({
        'get_config': get_config_data,
    })
