__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

from util import IOUtil

"""
    Wrapper for the configuration of Python application
"""


class Config(object):
    def __init__(self, config_file_name: str = 'conf/config.json'):
        """
        Constructor for configuration file
        :param config_file_name: Name of the JSON file containing the configuration parameters
        """
        ioutil = IOUtil(config_file_name)
        self.dict = ioutil.to_json()

    def __call__(self, key: str):
        """
            Access the attributed associated with this key
            :param key: Key or attribute name
            :return: Attributed if successful, None otherwise
        """
        try:
            return self.dict[key]
        except KeyError as e:
            print(f'Key error: {str(e)}')
            return None
        except AttributeError as e:
            print(f'Attributed error: {str(e)}')
            return None

