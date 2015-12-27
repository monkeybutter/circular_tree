from util import tree_planter, tree_pprinter, tree_bound_checker, tree_accuracy_meter, cxval_test
import time
import pandas as pd
import numpy as np
import argparse
import itertools

if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser(description="Tree parser")
    parser.add_argument(dest="path", type=str, help="path to csv")

    args = parser.parse_args()
    """

    names = ["eddt", "egll", "yssy", "zbaa", "lebl", "lfpg", "limc"]

    lin_vars = ['gfs_press', 'gfs_rh', 'gfs_temp', 'gfs_wind_spd']
    cir_vars = ['gfs_wind_dir', 'time', 'date']
    class_vars = ['metar_wind_spd']

    for class_var in class_vars:
        for i in range(0, len(lin_vars)+1):
            for lin_group in itertools.combinations(lin_vars, i):
                for j in range(1, len(cir_vars)+1):
                    for cir_group in itertools.combinations(cir_vars, j):

                        print(class_var, lin_group, cir_group)

                        rmse_a, rmse_b, rmse_c = [], [], []

                        for name in names:

                            df = pd.read_csv("./datasets/{}_clean.csv".format(name))

                            var_desc = {}
                            for lin_var in lin_group:
                                var_desc[lin_var] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

                            # 1 Classic
                            for cir_var in cir_group:
                                var_desc[cir_var] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

                            _, a = cxval_test(df, class_var, var_desc, 100, seed=1)
                            rmse_a.append(a)

                            # 2 Our
                            for cir_var in cir_group:
                                var_desc[cir_var] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}

                            _, b = cxval_test(df, class_var, var_desc, 100, seed=1)
                            rmse_b.append(b)

                            # 3 Lund
                            for cir_var in cir_group:
                                var_desc[cir_var] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}

                            _, c = cxval_test(df, class_var, var_desc, 100, seed=1)
                            rmse_c.append(c)

                        avg_a, avg_b, avg_c = sum(rmse_a)/len(rmse_a), sum(rmse_b)/len(rmse_b), sum(rmse_c)/len(rmse_c)
                        perc_a, perc_c = ((avg_a - avg_b) / avg_a) * 100, ((avg_c - avg_b) / avg_c) * 100

                        print("(A: {0:.3f}%, B: {1:.3f}%): Class: {2}, Our: {3}, Lund: {4}".format(perc_a, perc_c, avg_a, avg_b, avg_c))
