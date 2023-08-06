""" Delete Secret or Env Variable """
from mcli.config import MCLIConfig


def delete_environment_variable(variable_name: str, **kwargs) -> int:
    del kwargs
    conf = MCLIConfig.load_config()

    existing_env_variables = conf.environment_variables
    new_env_vars = [x for x in existing_env_variables if x.name != variable_name]
    if len(existing_env_variables) == len(new_env_vars):
        print(f'Unable to find env var with name: {variable_name}.'
              ' To see all existing env vars run `mcli get env`')
        return 1
    conf.environment_variables = new_env_vars
    conf.save_config()
    return 0


def delete_secret(secret_name: str, **kwargs) -> int:
    del kwargs
    conf = MCLIConfig.load_config()

    existing_secrets = conf.secrets
    new_secrets = [x for x in existing_secrets if x.name != secret_name]
    if len(existing_secrets) == len(new_secrets):
        print(f'Unable to find secret with name: {secret_name}.'
              ' To see all existing secrets run `mcli get secrets`')
        return 1
    conf.secrets = new_secrets
    conf.save_config()
    return 0
