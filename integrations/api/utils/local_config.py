import integrations.api.config.app_configuration as p

class LocalConfig(object):

    def __init__(self):
        pass

    def __getattr__(self, attr):
        return p.config[attr]

    def __getitem__(self, key):
        return p.config[key]