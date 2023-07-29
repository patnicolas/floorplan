

import numpy as np
from typing import List
import torch
from torch.autograd import Variable


class TorchBasics(object):
    def __init__(self, x: np.Array, shape: List[int], required_grad: bool):
        self.x = Variable(torch.from_numpy(x).view(shape), required_grad=required_grad)
        print(type(self.x))

    def __str__(self):
        print(f'Size: {self.x.size}\n{self.x.numpy()}')





if __name__ == '__main__':
    torch_basics = TorchBasics(np.array([1.0, 0.5, 0.25, 0.5, 1.0, 2.0]), [2, 4], True)



