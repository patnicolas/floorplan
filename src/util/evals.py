

def eval1():
    
    a = [1, 2, 3, 4]
    print(a[1:4])
    print(a[-2:])  # [3, 4]
    print(a[:-2])  # [1 , 2]
    a[:] = a[-2:] + a[:-2]
    print(a)
    import numpy as np
    a = np.linspace(0, 20, 20).reshape(5, 4)
    b = np.linspace(100, 105, 5).reshape(5, 1)
    try:
        z = a * b
        # print(f'Element wise multiplication shape {z.shape}\n{z}') # shape (5, 4)
        z = np.dot(a, b)
        print(
            f'Matrix multiplication shape {z.shape}\n{z}')  # shapes (5,4) and (5,1) not aligned: 4 (dim 1) != 5 (dim 0)
    except ValueError as e:
        print(str(e))  # shapes (5,4) and (5,1) not aligned: 4 (dim 1) != 5 (dim 0)

    c = np.linspace(200, 204, 4).reshape(4, 1)
    try:
        # z = a*c
        print(
            f'Element wise multiplication 2 shape  {z.shape}\n{z}')  # operands could not be broadcast together with shapes (5,4) (4,1)
        z = np.dot(a, c)  # Same as np.matmul(a, c) or a @ c
        print(f'Matrix multiplication 2 shape {z.shape}\n {z}')
    except ValueError as e:
        print(str(e))


def eval2():
    import numpy as np
    x = np.random.rand(4, 5)
    y = np.sum(x, axis=1)
    print (str(y.shape))


def eval3(value, lst):
    lst.append(value)
    return list


if __name__ == '__main__':
    import torch
    x = torch.rand(4, 4).to('mps')
    print(x)
    print(int(3 & 1))
    def foo():
        try:
            return 1
        finally:
            return 2
    k = foo()
    print(k)


    l1 = [1, 5, 6, 9]
    l2 = l1
    l3 = [1, 5, 6, 9]
    print(l1 is l3)
    print(l1 == l3)

    h = 'hacked'
    print(h[1:12])
    print(h[1:9][1:3])

    import numpy as np

    x = 2
    z = ++x
    print(f"++x {z}")
    y = x*z
    print(f"x: {x}")
    for i in range(3):
        print(f'i: {++i}')
    def multipliers():
        return [lambda x:i*x for i in range(4)]
    print([m(2) for m in multipliers()])    # [6, 6, 6, 6]

    x = np.zeros((3, 4))
    print(x.shape)
    v = np.random.randn((x.shape[0]))
    print(v.shape)


