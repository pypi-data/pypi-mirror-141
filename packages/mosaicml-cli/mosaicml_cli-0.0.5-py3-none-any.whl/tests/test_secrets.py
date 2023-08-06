from mcli.platform.secrets import (_create_docker_registry_secret, _create_generic_environment_secret,
                                   _create_generic_mounted_secret)
from mcli.utils.utils_kube import base64_encode


def test_docker_registry_secret_encoded():
    """Test that important docker registry secret fields are base64 encoded
    """
    values = {
        'docker_username': 'bar',
        'docker_password': 'abc123',
        'docker_email': 'bar@example.com',
        'docker_server': 'https://example.com'
    }
    docker_secret = _create_docker_registry_secret(secret_name='foo', **values)
    for key, value in values.items():
        assert getattr(docker_secret, key) == base64_encode(value)


def test_mounted_secret_encoded():
    """Test that important mounted secret fields are base64 encoded
    NOTE: `mount_path` is not stored in the secret object in k8s, so doesn't need to encoded
    """
    values = {'value': 'bar'}
    mounted_secret = _create_generic_mounted_secret(secret_name='foo', mount_path='/baz', **values)
    for key, value in values.items():
        assert getattr(mounted_secret, key) == base64_encode(value)


def test_env_secret_encoded():
    """Test that important env secret fields are base64 encoded
    NOTE: `env_key` is not stored in the secret object in k8s, so doesn't need to be encoded
    """
    values = {'value': 'bar'}
    env_secret = _create_generic_environment_secret(secret_name='foo', env_key='BAZ', **values)
    for key, value in values.items():
        assert getattr(env_secret, key) == base64_encode(value)
