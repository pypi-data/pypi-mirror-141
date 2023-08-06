from ruamel import yaml


class Yaml:
    @classmethod
    def stringify(cls, data):
        return yaml.load(data, Loader=yaml.RoundTripLoader)
        # return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)

    @classmethod
    def parse(cls, data):
        return yaml.safe_load(data)
