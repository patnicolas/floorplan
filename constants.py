__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

import torch
import os
import pathlib

if torch.cuda.is_available():
    torch_device = 'mps'
    torch_FloatTensor = torch.cuda
else:
    torch_device = 'cpu'
    torch_FloatTensor = torch.FloatTensor


# Set up folders from either unit-test or production
# It is assumed that test folder is a sub-directory of the given Python package
relative_path = pathlib.PurePath(os.getcwd()).name

print(f'Relative path: {relative_path}')
