from ruamel import yaml


# https://blog.csdn.net/BreezePython/article/details/108770195

class Yaml:
    @classmethod
    def stringify(cls, data):
        return yaml.load(data, Loader=yaml.RoundTripLoader)

    @classmethod
    def parse(cls, data):
        return yaml.safe_load(data)
