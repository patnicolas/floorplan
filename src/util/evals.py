

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


from typing import List
def eval4(input: List[int]) -> int:
    yy= [y*2 for y in input if y % 4 == 0]

    values = map(lambda x: x*2, filter(lambda x: x%4 ==0, input))
    values_iter = iter(values)
    state = True
    while state:
        try:
            print(next(values_iter))
        except Exception as e:
            state = False
    return sum(values)


if __name__ == '__main__':

    l = [[1, 2, 9], [4, 3, 4], [5, 1, 6]]
    ans =  list(map(min, l))  # [1, 3, 0]
    print(ans)


    def myfunc1():
        x = "John"

        def myfunc2():
            nonlocal x
            x = "hello"

        myfunc2()
        return x
    print(myfunc1())






