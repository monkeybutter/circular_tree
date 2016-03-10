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
    class_vars = ['metar_press', 'metar_rh', 'metar_temp', 'metar_wind_spd']

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

    """

    for name in names:
        print(name)

        #for leaf_size in [50, 100, 250]:
        for leaf_size in [100]:
            print(leaf_size)
            df = pd.read_csv("./datasets/{}_clean.csv".format(name))
            #df = df.drop(['gfs_press', 'gfs_rh', 'gfs_temp', 'gfs_wind_spd'], axis=1)
            df = df.drop(['date', 'time'], axis=1)
            df = df.drop(['metar_press', 'metar_rh', 'metar_temp'], axis=1)

            #metar_press,metar_rh,metar_temp,metar_wind_spd,gfs_press,gfs_rh,gfs_temp,gfs_wind_dir,gfs_wind_spd,time,date

            var_desc = {}
            var_desc["gfs_press"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc["gfs_rh"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc["gfs_temp"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc["gfs_wind_dir"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc["gfs_wind_spd"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            #var_desc["time"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            #var_desc["date"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

            class_var = 'metar_wind_spd'

            a_mae = []
            a_rmse = []
            a_time = []

            b_mae = []
            b_rmse = []
            b_time = []

            c_mae = []
            c_rmse = []
            c_time = []

            for i in range(1):

                #print("A")
                var_desc["gfs_wind_dir"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                #var_desc["time"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                #var_desc["date"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                a_mae.append(mae)
                a_rmse.append(rmse)
                a_time.append(time.time()-time1)
                #print(i)

                #print("B")
                var_desc["gfs_wind_dir"] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                #var_desc["time"] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                #var_desc["date"] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                b_mae.append(mae)
                b_rmse.append(rmse)
                b_time.append(time.time()-time1)

                #print("C")
                var_desc["gfs_wind_dir"] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}
                #var_desc["time"] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}
                #var_desc["date"] = {"type": "lin", "method": "subset", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                c_mae.append(mae)
                c_rmse.append(rmse)
                c_time.append(time.time()-time1)

            print("{}, {}".format(sum(a_rmse)/len(a_rmse), sum(a_time)/len(a_time)))
            print("{}, {}".format(sum(b_rmse)/len(b_rmse), sum(b_time)/len(b_time)))
            print("{}, {}".format(sum(c_rmse)/len(c_rmse), sum(c_time)/len(c_time)))

    for name in names:
        print(name)

        #for leaf_size in [50, 100, 250]:
        for leaf_size in [100]:
            print(leaf_size)
            df = pd.read_csv("./datasets/{}_clean.csv".format(name))
            df = df.drop(["gfs_press", 'gfs_wind_spd', 'date', 'time'], axis=1)
            df = df.drop(['metar_rh', 'metar_wind_spd'], axis=1)

            #metar_press,metar_rh,metar_temp,metar_wind_spd,gfs_press,gfs_rh,gfs_temp,gfs_wind_dir,gfs_wind_spd,time,date

            var_desc = {}
            var_desc['gfs_wind_dir'] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc['gfs_temp'] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc['gfs_rh'] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

            class_var = 'metar_press'

            a_mae = []
            a_rmse = []
            a_time = []

            b_mae = []
            b_rmse = []
            b_time = []

            c_mae = []
            c_rmse = []
            c_time = []

            for i in range(1):

                #print("A")
                var_desc['gfs_wind_dir'] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                #var_desc["date"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                a_mae.append(mae)
                a_rmse.append(rmse)
                a_time.append(time.time()-time1)
                #print(i)

                #print("B")
                var_desc['gfs_wind_dir'] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                #var_desc["date"] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                b_mae.append(mae)
                b_rmse.append(rmse)
                b_time.append(time.time()-time1)

                #print("C")
                var_desc['gfs_wind_dir'] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}
                #var_desc["date"] = {"type": "lin", "method": "subset", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                c_mae.append(mae)
                c_rmse.append(rmse)
                c_time.append(time.time()-time1)

            print("{}, {}".format(sum(a_rmse)/len(a_rmse), sum(a_time)/len(a_time)))
            print("{}, {}".format(sum(b_rmse)/len(b_rmse), sum(b_time)/len(b_time)))
            print("{}, {}".format(sum(c_rmse)/len(c_rmse), sum(c_time)/len(c_time)))
    """