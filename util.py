import numpy as np
from data.classic_data import ClassicData
from data.subset_data import SubsetData
from node.node import Node


##### accuracy evaluator (value accumulator) #########
def var_calc(anode):
    return np.var(anode.data.df[anode.data.class_var].values)


def tree_accuracy_meter(node):
    acc = 0.0
    total_len = len(node.data.df.index)

    def walk_tree(node):
        nonlocal acc

        if node.left_child is None:
            acc += len(node.data.df.index) * np.var(node.data.df[node.data.class_var].values)

        else:
            walk_tree(node.left_child)
            walk_tree(node.right_child)

    walk_tree(node)

    return acc / total_len



##### correctness evaluator (True/False) #######

def bound_checker(bounds):
    prev = (None, None)

    for bound in bounds:
        if not bound[0] < bound[1]:
            return False
        if None not in prev and prev[1] >= bound[0]:
            return False

        prev = bound

    return True


def tree_bound_checker(node):
    valid = True

    def walk_tree(node):
        nonlocal valid

        for var_bounds in [node.data.var_desc[key]['bounds'] for key in node.data.var_desc.keys()]:

            if not bound_checker(var_bounds):
                valid = False
                print("Bound error: ", var_bounds)


        if node.left_child is not None:
            walk_tree(node.left_child)
            walk_tree(node.right_child)

    walk_tree(node)

    return valid


    
def tree_pprinter(node):
    fmtr = ""

    def pprinter(anode):
        nonlocal fmtr

        if anode.split_var is not None:
            print("({}) {} {}".format(len(anode.data.df.index), anode.split_var,
                                       anode.data.var_desc[anode.split_var]['bounds']))

        else:
            print("({}) Leaf {} {}".format(len(anode.data.df.index),
                                    np.var(anode.data.df[anode.data.class_var].values), ["{} {}".format(key, anode.data.var_desc[key]['bounds']) for key in anode.data.var_desc.keys()]))


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


def tree_planter(df, class_var, input_vars, var_types, tree_type='classic', stop=50, variance=.2):
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
                #var_desc[input_var] = {"name": input_var, "type": "lin", "bounds": [[-np.inf, np.inf]]}
                var_desc[input_var] = {"type": "lin", "bounds": [[-np.inf, np.inf]]}
            elif var_types[i] == "cir":
                #var_desc[input_var] = {"name": input_var, "type": "cir", "bounds": [[-np.inf, np.inf]]}
                var_desc[input_var] = {"type": "cir", "bounds": [[-np.inf, np.inf]]}


        if tree_type == 'classic':
            data = ClassicData(df, class_var, var_desc)
        elif tree_type == 'subset':
            data = SubsetData(df, class_var, var_desc)

        node = Node(data, stop=stop, variance=variance)
        node.split()

        return node