from util import tree_planter, tree_pprinter, tree_bound_checker, tree_accuracy_meter, cxval_test
import time
import pandas as pd
import numpy as np
import argparse
import itertools

if __name__ == "__main__":

    names = ["eddt", "egll", "yssy", "zbaa", "lebl", "lfpg", "limc"]

    lin_group = ['gfs_wind_spd', 'gfs_rh']
    cir_group = ['time', 'date']
    class_var = 'metar_temp'

    print(class_var, lin_group, cir_group)

    for name in names:

        #for bin_size in [50, 100, 250]:
        for bin_size in [50, 100, 250, 500, 1000, 2500]:
            rmse_a, rmse_b, rmse_c = [], [], []
            time_a, time_b, time_c = [], [], []

            df = pd.read_csv("./datasets/{}_clean.csv".format(name))

            var_desc = {}
            for lin_var in lin_group:
                var_desc[lin_var] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

            # 1 Classic
            for cir_var in cir_group:
                var_desc[cir_var] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

            time1 = time.time()
            _, a = cxval_test(df, class_var, var_desc, bin_size, seed=1)
            time_a.append(time.time()-time1)
            rmse_a.append(a)
            print(1)

            # 2 Our
            for cir_var in cir_group:
                var_desc[cir_var] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}

            time1 = time.time()
            _, b = cxval_test(df, class_var, var_desc, bin_size, seed=1)
            time_b.append(time.time()-time1)
            rmse_b.append(b)
            print(2)

            # 3 Lund
            for cir_var in cir_group:
                var_desc[cir_var] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}

            time1 = time.time()
            _, c = cxval_test(df, class_var, var_desc, bin_size, seed=1)
            time_c.append(time.time()-time1)
            rmse_c.append(c)
            print(3)

            avg_a, avg_b, avg_c = sum(rmse_a)/len(rmse_a), sum(rmse_b)/len(rmse_b), sum(rmse_c)/len(rmse_c)
            avg_time_a, avg_time_b, avg_time_c = sum(time_a)/len(time_a), sum(time_b)/len(time_b), sum(time_c)/len(time_c)

            print("Times: Class: {0}, Our: {1}, Lund: {2}".format(avg_time_a, avg_time_b, avg_time_c))
            print("(Airport: {0} - Bin Size: {1}): Class: {2}, Our: {3}, Lund: {4}".format(name, bin_size, avg_a, avg_b, avg_c))