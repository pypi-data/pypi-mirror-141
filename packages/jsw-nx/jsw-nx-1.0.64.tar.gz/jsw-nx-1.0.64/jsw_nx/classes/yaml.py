from ruamel import yaml


class Yaml:
    @classmethod
    def stringify(cls, data):
        return yaml.dump(
            data,
            allow_unicode=True,
            default_flow_style=False,
            line_break=True,
            Dumper=yaml.RoundTripDumper
        )

    @classmethod
    def parse(cls, data):
        return yaml.load(data, Loader=yaml.RoundTripLoader)
