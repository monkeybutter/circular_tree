import numpy as np
import pandas as pd
from random import random, randint

def randomizer(i0, i1, prob):
    if random() < prob and i0 < i1-1:
        new_i0 = randint(i0, i1-1)
        new_i1 = randint(new_i0+1, i1)
        return (new_i0, new_i1)
    else:
        return None

def splitter(i, j):
    if j-i > 2:
        return randint(i+1, j-1)
    else:
        return None
    
    
def create_simple_data(size):
    input_a = np.sort(np.random.uniform(low=0.0, high=1000.0, size=size))
    
    i = 0
    class_var = np.random.normal(i, .1, size=size)
    
    a, b = 0, size-1
    
    while True:
        i += 1
        bounds = randomizer(a, b, .8)
        if bounds is None:
            break
        class_var[a:b] = np.random.normal(i, .1, size=b-a)
        a, b = bounds
    
    return pd.DataFrame(np.vstack((input_a, class_var)).T, columns=['input1', 'class_var'])


def create_simple_data2(size, min_size):

    input_a = np.sort(np.random.uniform(low=0.0, high=1000.0, size=size))

    class_var = np.zeros(size)

    def write_chunk(i, j, min_size, level):

        class_var[i:j] = np.random.normal(level, .1, size=j-i)
        k = splitter(i, j)

        if k-i > min_size:
            write_chunk(i, k, min_size, level+1)
        if j-k > min_size:
            write_chunk(k, j, min_size, level+1)

    write_chunk(0, size-1, min_size, 0)


    return pd.DataFrame(np.vstack((input_a, class_var)).T, columns=['input1', 'class_var'])