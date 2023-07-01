__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

import os
import pathlib

# Set up folders from either unit-test or production
# It is assumed that test folder is a sub-directory of the given Python package
relative_path = pathlib.PurePath(os.getcwd()).name

print(f'Relative path: {relative_path}')
