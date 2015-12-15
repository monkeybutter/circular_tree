from util import tree_planter, tree_pprinter, tree_bound_checker, tree_accuracy_meter
import time
import pandas as pd
import numpy as np
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Tree parser")
    parser.add_argument(dest="path", type=str, help="path to csv")

    args = parser.parse_args()
    df = pd.read_csv(args.path)

    var_desc = {}
    var_desc["gfs_press"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_rh"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_temp"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_wind_dir"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["gfs_wind_spd"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["time"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}
    var_desc["date"] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

    class_var = "metar_wind_spd"

    time1 = time.time()
    tree_classic = tree_planter(df, class_var, var_desc, 250, 0.25)
    tree_pprinter(tree_classic)
    print("Check bounds: {}".format(tree_bound_checker(tree_classic)))
    print("Accuracy: {}".format(tree_accuracy_meter(tree_classic)))
    time2 = time.time()
    print("Classic function took {0:.2f} s".format((time2-time1)))