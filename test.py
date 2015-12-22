from util import tree_planter, tree_pprinter, tree_bound_checker, tree_accuracy_meter, cxval_test
import time
import pandas as pd
import numpy as np
import argparse

if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser(description="Tree parser")
    parser.add_argument(dest="path", type=str, help="path to csv")

    args = parser.parse_args()
    """

    names = ["eddt", "egll", "yssy", "zbaa", "lebl", "lfpg", "limc"]

    for name in names:
        print(name)

        for leaf_size in [50, 100, 250]:
            print(leaf_size)
            df = pd.read_csv("./datasets/{}_clean.csv".format(name))
            df = df.drop(["time", "date", "gfs_wind_spd", "gfs_rh"], axis=1)
            df = df.drop(['metar_press', 'metar_temp', 'metar_rh'], 1)

            var_desc = {}
            var_desc["gfs_press"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            #var_desc["gfs_rh"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc["gfs_temp"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            var_desc["gfs_wind_dir"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            #var_desc["gfs_wind_spd"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            #var_desc["time"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
            #var_desc["date"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

            class_var = "metar_wind_spd"

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
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                a_mae.append(mae)
                a_rmse.append(rmse)
                a_time.append(time.time()-time1)
                #print(i)

                #print("B")
                var_desc["gfs_wind_dir"] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                b_mae.append(mae)
                b_rmse.append(rmse)
                b_time.append(time.time()-time1)

                #print("C")
                var_desc["gfs_wind_dir"] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}
                time1 = time.time()
                mae, rmse = cxval_test(df, class_var, var_desc, leaf_size, seed=i)
                c_mae.append(mae)
                c_rmse.append(rmse)
                c_time.append(time.time()-time1)

            print("Classic Accuracy: MAE: {}, RMSE: {}, Time: {}".format(sum(a_mae)/len(a_mae), sum(a_rmse)/len(a_rmse),
                                                                         sum(a_time)/len(a_time)))
            print("Our Accuracy: MAE: {}, RMSE: {}, Time: {}".format(sum(b_mae)/len(b_mae), sum(b_rmse)/len(b_rmse),
                                                                     sum(b_time)/len(b_time)))
            print("Lunds Accuracy: MAE: {}, RMSE: {}, Time: {}".format(sum(c_mae)/len(c_mae), sum(c_rmse)/len(c_rmse),
                                                                       sum(c_time)/len(c_time)))