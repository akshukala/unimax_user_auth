CONFIG_MAP = {
    'prod': 'production',
    'dev': 'development'
}

def get_config(env):
    return '.'.join(['userservice', 'conf', 'environments',
                     CONFIG_MAP.get(env, env), 'Config'])
