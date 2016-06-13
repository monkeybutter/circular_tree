from util import tree_planter, tree_pprinter, tree_rmse_calc
import time
import pandas as pd
import numpy as np

if __name__ == "__main__":

    lin_group = []
    cir_group = ['prec', 'tilt']
    class_var = 'rad'

    print(class_var, lin_group, cir_group)

    #for bin_size in [2500, 1800]:
    for bin_size in [2500, 2250, 2000, 1750, 1500, 1250, 1000, 750, 500, 250]:
        print(bin_size)

        df = pd.read_csv("./datasets/false_hope.csv")
        rmse = []

        var_desc = {}
        for lin_var in lin_group:
            var_desc[lin_var] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

        # 1 Classic
        for cir_var in cir_group:
            var_desc[cir_var] = {"type": "lin", "method": "classic", "bounds": [[-np.inf, np.inf]]}

        time1 = time.time()
        tree = tree_planter(df, class_var, var_desc, bin_size, .01)
        #tree_pprinter(tree)
        rmse.append(tree_rmse_calc(tree, df))

        # 2 Our
        for cir_var in cir_group:
            var_desc[cir_var] = {"type": "cir", "method": "classic", "bounds": [[-np.inf, np.inf]]}

        time1 = time.time()
        tree = tree_planter(df, class_var, var_desc, bin_size, .01)
        #tree_pprinter(tree)
        rmse.append(tree_rmse_calc(tree, df))

        # 3 Lund
        for cir_var in cir_group:
            var_desc[cir_var] = {"type": "cir", "method": "subset", "bounds": [[-np.inf, np.inf]]}

        time1 = time.time()
        tree = tree_planter(df, class_var, var_desc, bin_size, .01)
        #tree_pprinter(tree)
        rmse.append(tree_rmse_calc(tree, df))

        print(rmse)

