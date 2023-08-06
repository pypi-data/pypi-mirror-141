"""
Test some basic truths about our YAML configuration file structure
"""
from pathlib import Path
from typing import List

import pytest
import yaml

from mcli.sweeps.local_sweep_config import RunType
from mcli.utils.utils_file import list_yamls

YAML_DIR = Path(__file__).parents[1].joinpath('yamls')
DEFAULTS = YAML_DIR.joinpath('defaults')
OVERRIDES = YAML_DIR.joinpath('model-specific')


def get_yaml_names(directory: Path) -> List[str]:
    return [f.stem for f in list_yamls(directory)]


MODELS = get_yaml_names(DEFAULTS.joinpath('models'))
INSTANCES = get_yaml_names(DEFAULTS.joinpath('instances'))
LOGGERS = get_yaml_names(DEFAULTS.joinpath('loggers'))
RUN_TYPES = get_yaml_names(DEFAULTS.joinpath('run_types'))


def check_yaml_non_empty(yaml_file: Path) -> bool:
    with open(yaml_file, 'r') as fh:
        data = yaml.safe_load(fh)
    if isinstance(data, dict) and len(data):
        return True
    else:
        return False


@pytest.mark.parametrize('model', MODELS)
def test_model_yamls_non_empty(model: str):
    """Check that every model yaml file is not empty

    Args:
        model (str): Name of the model
    """
    yaml_file = DEFAULTS.joinpath('models', f'{model}.yaml')
    assert yaml_file.exists()
    assert check_yaml_non_empty(yaml_file)


@pytest.mark.parametrize('model', MODELS)
def test_model_specific_directory_exists(model: str):
    """Check that all models listed have a corresponding 'model-specific' subdirectory.
    """
    specific_dir = OVERRIDES.joinpath(model)
    assert specific_dir.exists() and specific_dir.is_dir()


@pytest.mark.parametrize('instance', INSTANCES)
def test_instance_yamls_non_empty(instance: str):
    """Check that every instance yaml file is not empty

    Args:
        instance (str): Name of the instance
    """
    yaml_file = DEFAULTS.joinpath('instances', f'{instance}.yaml')
    assert yaml_file.exists()
    assert check_yaml_non_empty(yaml_file)


@pytest.mark.parametrize('model', MODELS)
def test_model_specific_instances_valid(model: str):
    """Check that all override instance types have a corresponding set of defaults

    Args:
        model (str): Name of the model to check
    """
    model_instances = get_yaml_names(OVERRIDES.joinpath(model, 'instances'))

    # xfail if there are no instance overrides
    if len(model_instances) == 0:
        pytest.xfail(f'No instance yamls for model {model}')
    else:
        assert all(instance in INSTANCES for instance in model_instances)


@pytest.mark.parametrize('run_type', RUN_TYPES)
def test_valid_run_type(run_type: str):
    """Test that every listed run type is valid

    Args:
        run_type (str): Name of the run type
    """
    try:
        rt = RunType[run_type.upper()]
    except KeyError:
        pytest.fail("Invalid run type. All yamls in the 'run_types' subdirectory should be valid values of RunType")
