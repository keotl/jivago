import yaml


class ApplicationProperties(object):

    def __init__(self, content: dict):
        self.content = content

    def __getitem__(self, item):
        return self.content[item]


def load_yaml_config(filename: str) -> ApplicationProperties:
    with open(filename, 'r') as stream:
        return ApplicationProperties(yaml.load(stream))
