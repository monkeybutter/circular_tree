from util import tree_planter, tree_pprinter, tree_bound_checker, tree_accuracy_meter
import time
import pandas as pd
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Tree parser")
    parser.add_argument(dest="path", type=str, help="path to csv")

    args = parser.parse_args()

    df = pd.read_csv(args.path)

    #df = df.drop(['gfs_press', 'gfs_rh', 'date', 'time'], 1)

    cols = list(df.columns)

    class_var = cols[0]
    del cols[0]
    input_vars = cols
    type_vars = ['lin' for var in input_vars]
    method_vars = ['classic' for var in input_vars]

    time1 = time.time()
    tree_classic = tree_planter(df, class_var, input_vars, type_vars, method_vars, 250, 0.25)
    tree_pprinter(tree_classic)
    print("Check bounds: {}".format(tree_bound_checker(tree_classic)))
    print("Accuracy: {}".format(tree_accuracy_meter(tree_classic)))
    time2 = time.time()
    print("Classic function took {0:.2f} s".format((time2-time1)))

    type_vars[3] = 'cir'
    type_vars[5] = 'cir'
    type_vars[6] = 'cir'

    time1 = time.time()
    tree_subset = tree_planter(df, class_var, input_vars, type_vars, method_vars, 250, 0.25)
    tree_pprinter(tree_subset)
    print("Check bounds: {}".format(tree_bound_checker(tree_subset)))
    print("Accuracy: {}".format(tree_accuracy_meter(tree_subset)))
    time2 = time.time()
    print("Subset function took {0:.2f} s".format((time2-time1)))

    type_vars[3] = 'lin'
    type_vars[5] = 'lin'
    type_vars[6] = 'lin'
    method_vars = ['subset' for var in input_vars]

    time1 = time.time()
    tree_subset = tree_planter(df, class_var, input_vars, type_vars, method_vars, 250, 0.25)
    tree_pprinter(tree_subset)
    print("Check bounds: {}".format(tree_bound_checker(tree_subset)))
    print("Accuracy: {}".format(tree_accuracy_meter(tree_subset)))
    time2 = time.time()
    print("Subset function took {0:.2f} s".format((time2-time1)))

    type_vars[3] = 'cir'
    type_vars[5] = 'cir'
    type_vars[6] = 'cir'

    time1 = time.time()
    tree_subset = tree_planter(df, class_var, input_vars, type_vars, method_vars, 250, 0.25)
    tree_pprinter(tree_subset)
    print("Check bounds: {}".format(tree_bound_checker(tree_subset)))
    print("Accuracy: {}".format(tree_accuracy_meter(tree_subset)))
    time2 = time.time()
    print("Subset function took {0:.2f} s".format((time2-time1)))