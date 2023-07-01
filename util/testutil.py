__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

from typing import AnyStr, Dict, Optional


class TestUtil(object):
    def __init__(self, test_file: AnyStr):
        """
        Constructor for the test parameters CSV file
        :param test_file: Name of the test configuration file
        """
        self.test_file = test_file

    def load_test_variables(self) -> Optional[Dict[AnyStr, AnyStr]]:
        """
        Load the test variables as an option of a dictionary
        :return: Optional dictionary
        """
        try:
            with open(self.test_file, 'rt') as f:
                rows = f.read().split("\n")
                acc = {}
                for row in rows:
                    key_value = row.split(",")
                    acc[key_value[0]] = key_value[1]
            return acc
        except FileNotFoundError as e:
            print(str(e))
            return None
        except Exception as e:
            print(str(e))
            return None


if __name__ == '__main__':
    test_util = TestUtil('../test_input/test.csv')
    dictionary = test_util.load_test_variables()
    print(str(dictionary))
