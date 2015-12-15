import numpy as np
from data.data import Data
from node.node import Node
import random
import copy


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

        for desc in [node.data.var_desc[key] for key in node.data.var_desc.keys()]:

            if not bound_checker(desc['bounds']) and desc['type'] == 'lin':
                valid = False
                print("Bound error: ", desc['bounds'])


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
                                    np.var(anode.data.df[anode.data.class_var].values),
                                           ["{} {}".format(key, anode.data.var_desc[key]['bounds']) for key in anode.data.var_desc.keys() if anode.data.var_desc[key]['bounds'] != [[-np.inf, np.inf]]]))


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


def tree_planter(df, class_var, var_desc, stop=50, variance=.2):
        if class_var not in df.columns:
            raise Exception('Class variable not in DataFrame')

        data = Data(df, class_var, var_desc)

        node = Node(data, stop=stop, variance=variance)
        node.split()

        return node


# Input tree and row
# Output collection of rows
def tree_eval(node, row):
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


def cxval_k_folds_split(df, k_folds):

    dataframes = []
    group_size = int(round(df.shape[0]*(1.0/k_folds)))

    for i in range(k_folds-1):
        rows = random.sample(df.index, group_size)
        dataframes.append(df.ix[rows])
        df = df.drop(rows)

    dataframes.append(df)

    return dataframes


def cxval_select_fold(i_fold, df_folds):
    df_folds_copy = copy.deepcopy(df_folds)

    if 0 <= i_fold < len(df_folds):

        test_df = df_folds_copy[i_fold]
        del df_folds_copy[i_fold]
        train_df = pd.concat(df_folds_copy)

        return train_df, test_df

    else:
        raise Exception('Group not in range!')


def cxval_test(df, class_var, var_desc, bin_size, k_folds):

    df_folds = cxval_k_folds_split(df, k_folds)
    results = []

    for i in range(k_folds):
        print("Cross Validation: {}".format(i+1))
        train_df, test_df = cxval_select_fold(i, df_folds)
        tree = tree_planter(train_df, class_var, var_desc)

        print("Cross Correlation: {}".format(evaluate_dataset_cc(tree, test_df)))
        print("Root Mean Square Error: {}".format(evaluate_dataset_rmse(tree, test_df)))
        print("Mean Absolute Error: {}".format(evaluate_dataset_mae(tree, test_df)))