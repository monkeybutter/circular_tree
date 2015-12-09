import numpy as np
import pandas as pd
from random import random, randint
from data.classic_data import ClassicData
from data.subset_data import SubsetData
from node.node import Node


def bound_checker(bounds):
    
    prev = (None, None)
    
    for bound in bounds:
        if not bound[0] < bound[1]:
            return False
        if None not in bound and prev[1] >= bound[0]:     
            return False
            
        prev = bound
        
    return True


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

    
def tree_pprinter(node):
    fmtr = ""

    def pprinter(anode):
        nonlocal fmtr

        if anode.split_var is not None:
            print("({}) {}, {}".format(len(anode.data.df.index), anode.split_var,
                                       anode.data.var_desc[anode.split_var]['bounds']))
        else:
            print("({}) Leaf {}, {}".format(len(anode.data.df.index),
                                     anode.data.var_desc['gfs_wind_dir']['bounds'],
                                    np.var(anode.data.df[anode.data.class_var].values)))

        if anode.left_child is not None:
            print("{} `--".format(fmtr), end="")
            fmtr += "  | "
            pprinter(anode.left_child)
            fmtr = fmtr[:-4]

            print("{} `--".format(fmtr), end="")
            fmtr += "    "
            pprinter(anode.right_child)
            fmtr = fmtr[:-4]

    return pprinter(node)


def tree_planter(df, class_var, input_vars, var_types, stop=50, variance=.2):
        if class_var not in df.columns:
            raise Exception('Class variable not in DataFrame')

        for input_var in input_vars:
            if input_var not in df.columns:
                raise Exception('Input variable: "{}" not in DataFrame'.format(input_var))

        if class_var in input_vars:
            raise Exception('Class variable cannot be an input variable at the same time')

        if len(input_vars)+1 != len(var_types):
            raise Exception('Variable types must contain a list of the types for the class variable and input variables as: ["linear"|"circular"]')

        var_desc = {}
        for i, input_var in enumerate(input_vars):
            if var_types[i] == "lin":
                var_desc[input_var] = {"name": input_var, "type": "lin", "bounds": [[-np.inf, np.inf]]}
            elif var_types[i] == "cir":
                var_desc[input_var] = {"name": input_var, "type": "cir", "bounds": [[-np.inf, np.inf]]}


        data = ClassicData(df, class_var, var_desc)
        #data = SubsetData(df, class_var, var_desc)
        node = Node(data, stop=stop, variance=variance)
        node.split()

        return node