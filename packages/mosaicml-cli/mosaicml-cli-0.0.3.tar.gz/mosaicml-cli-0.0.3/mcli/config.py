"""Global Singleton Config Store"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List

import ruamel.yaml
import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from mcli.config_objects import MCLIEnvironmentItem, MCLIPlatform, MCLISecret, SerializableDataclass
from mcli.utils.utils_modules import check_if_module_exists
from mcli.utils.utils_yaml import StringDumpYAML

DEFAULT_CONFIG_DIR: Path = Path(os.path.expanduser('~/.mosaic'))
DEFAULT_PROJECTS_DIR: Path = Path(os.path.expanduser('~/.mosaic/projects'))
DEFAULT_CURRENT_PROJECT_SYMLINK_PATH: Path = Path(os.path.expanduser('~/.mosaic/current_project'))
DEFAULT_CONFIG_PATH: Path = Path(os.path.expanduser('~/.mosaic/config'))
CONFIG_PATH_ENVVAR: str = 'MOSAICCONFIG'
if CONFIG_PATH_ENVVAR in os.environ:
    DEFAULT_CONFIG_PATH = Path(os.environ[CONFIG_PATH_ENVVAR])

GRAPHQL_ENDPOINT: str = 'https://dat.int.mosaicml.com/api/graphql'

logging.getLogger('urllib3.connectionpool').disabled = True
MCLI_CONFIG_PATH: Path = Path(os.path.expanduser('~/.mosaic/mcli_config'))
COMPOSER_INSTALLED: bool = check_if_module_exists('composer')


class FeatureFlag(Enum):
    USE_FEATUREDB = 'USE_FEATUREDB'
    USE_PLATFORMS_FUTURE = 'USE_PLATFORMS_FUTURE'
    DEPRECATED_WANDB_KEY = 'DEPRECATED_WANDB_KEY'
    DEPRECATED_SSH_KEY = 'DEPRECATED_SSH_KEY'


@dataclass
class MCLIConfig(SerializableDataclass):
    """Global Config Store persisted on local disk"""

    DAT_API_KEY: str  # pylint: disable=invalid-name Global Stored within Singleton

    # Also settable through environment variable
    # MCLI_MODE=DEV
    dev_mode: bool = False
    _temporary_dev_mode = False
    _original_dev_mode_settings = False

    feature_flags: Dict[str, bool] = field(default_factory=dict)

    # Global Environment Variables
    environment_variables: List[MCLIEnvironmentItem] = field(default_factory=list)

    # Global Secrets
    secrets: List[MCLISecret] = field(default_factory=list)

    # Registered Platforms
    platforms: List[MCLIPlatform] = field(default_factory=list)

    @classmethod
    def generate_new_config(cls) -> MCLIConfig:
        return MCLIConfig(DAT_API_KEY='')

    def apply_dev_mode_environment_override(self):
        if os.environ.get('MCLI_MODE', None):
            self._temporary_dev_mode = True
            self._original_dev_mode_settings = self.dev_mode
            if os.environ.get('MCLI_MODE', 'DEV'):
                self.dev_mode = True
            elif os.environ.get('MCLI_MODE', 'PROD'):
                self.dev_mode = False

    @classmethod
    def load_config(cls) -> MCLIConfig:
        """Loads the MCLIConfig from local disk

        Return:
            Returns the MCLIConfig if successful, otherwise raises Exception
        """
        with open(MCLI_CONFIG_PATH, 'r', encoding='utf8') as f:
            data = yaml.full_load(f)
        conf = MCLIConfig.from_dict(data)
        conf.apply_dev_mode_environment_override()

        return conf

    def save_config(self) -> bool:
        """Saves the MCLIConfig to local disk

        Return:
            Returns true if successful
        """
        if self.dev_mode:
            print('saving config...')
        if self._temporary_dev_mode:
            self.dev_mode = self._original_dev_mode_settings
        data = self._get_formatted_dump()
        y = YAML()
        y.explicit_start = True  # type: ignore
        with open(MCLI_CONFIG_PATH, 'w', encoding='utf8') as f:
            y.dump(data, f)
        if self._temporary_dev_mode:
            self.apply_dev_mode_environment_override()
        return True

    def _get_formatted_dump(self) -> CommentedMap:
        """Gets the ruamel yaml formatted dump of the config
        """
        raw_data = self.to_dict()

        # Moves platforms to last item
        platforms = raw_data['platforms']
        del raw_data['platforms']
        raw_data['platforms'] = platforms

        data: CommentedMap = ruamel.yaml.load(
            yaml.dump(raw_data),
            ruamel.yaml.RoundTripLoader,
        )
        data.yaml_set_start_comment('MCLI Config Data\n')
        data.yaml_set_comment_before_after_key(
            key='DAT_API_KEY',
            before='API KEY for DAT',
        )
        data.yaml_set_comment_before_after_key(
            key='environment_variables',
            before='\nAll Gloabl Environment variables go here',
        )
        data.yaml_set_comment_before_after_key(
            key='secrets',
            before='\nAll Gloabl Secrets go here',
        )
        data.yaml_set_comment_before_after_key(
            key='platforms',
            before='\nAll Platforms configured for MCLI',
        )
        return data

    def feature_enabled(self, feature: FeatureFlag) -> bool:
        """Checks if the feature flag is enabled

        Args:
            feature (FeatureFlag): The feature to check
        """
        if feature.value in self.feature_flags:
            enabled = self.feature_flags[feature.value]
            return bool(enabled)
        return False

    def __str__(self) -> str:
        data = self._get_formatted_dump()
        y = StringDumpYAML()
        return y.dump(data)


def feature_enabled(feature: FeatureFlag) -> bool:
    conf = get_mcli_config()
    return conf.feature_enabled(feature=feature)


def get_mcli_config() -> MCLIConfig:
    try:
        return MCLIConfig.load_config()
    except FileNotFoundError:
        return MCLIConfig.generate_new_config()
