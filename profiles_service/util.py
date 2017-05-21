import os


def get_env_var(var_name, default_value=None):
    if var_name not in os.environ:
        return default_value

    return os.environ.get(var_name)
