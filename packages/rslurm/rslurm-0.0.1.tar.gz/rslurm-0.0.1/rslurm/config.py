import os

import yaml
import json


class Config(object):
    def __init__(self, config):
        for key, value in config.items():
            if key == 'local_path':
                value = os.path.abspath(value)
            setattr(self, key, value)

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)


def load_config(path='rslurm.yaml'):
    """

    Parameters
    ----------
    path

    Returns
    -------

    """
    with open(path, 'r') as stream:
        try:
            return Config(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            raise exc
