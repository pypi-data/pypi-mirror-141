import yaml


class Yaml:
    @classmethod
    def stringify(cls, data):
        return yaml.dump(data)

    @classmethod
    def parse(cls, data):
        return yaml.safe_load(data)
