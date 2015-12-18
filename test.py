from util import tree_planter, tree_pprinter, tree_bound_checker, tree_accuracy_meter, cxval_test
import time
import pandas as pd
import numpy as np
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Tree parser")
    parser.add_argument(dest="path", type=str, help="path to csv")

    args = parser.parse_args()
    df = pd.read_csv(args.path)

    df = df.drop(["time", "date"], axis=1)

    var_desc = {}
    var_desc["gfs_press"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_rh"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_temp"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_wind_dir"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_wind_spd"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
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

    for i in range(10):
        var_desc["gfs_wind_dir"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
        time1 = time.time()
        mae, rmse = cxval_test(df, class_var, var_desc, 100, seed=i)
        a_mae.append(mae)
        a_rmse.append(rmse)
        a_time.append(time.time()-time1)

        var_desc["gfs_wind_dir"] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}
        time1 = time.time()
        mae, rmse = cxval_test(df, class_var, var_desc, 100, seed=i)
        b_mae.append(mae)
        b_rmse.append(rmse)
        b_time.append(time.time()-time1)

        var_desc["gfs_wind_dir"] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}
        time1 = time.time()
        mae, rmse = cxval_test(df, class_var, var_desc, 100, seed=i)
        c_mae.append(mae)
        c_rmse.append(rmse)
        c_time.append(time.time()-time1)

    print("Classic Accuracy: {}").format(sum(a_mae)/len(a_mae))
    print("Our Accuracy: {}").format(sum(b_mae)/len(b_mae))
    print("Lunds Accuracy: {}").format(sum(c_mae)/len(c_mae))