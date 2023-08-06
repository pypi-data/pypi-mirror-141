import numpy as np
# from numpy.random import normal


def add(params0, params1):
    return params0 + params1


def square_plus_constant(z, constant):
    # print(globals())
    # print(globals()["testValue"])
    # print(testValue)
    return np.square(z) + constant


def double(param, add1, add2):
    return np.square(param) + add1 - add2


# def normal(**kwargs):
#     return np.random.normal(**kwargs)
