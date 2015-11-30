from util import tree_planter, tree_pprinter
import numpy as np
import pandas as pd



"""
# Test Classic Tree
input_var1 = np.arange(0, 10)
class_var = np.concatenate((np.random.normal(10, .1, 2),
                            np.random.normal(15, .1, 2),
                            np.random.normal(50, .1, 3),
                            np.random.normal(60, .1, 3)), axis=0)
"""
# Test Subset Tree
input_var1 = np.arange(0, 6)
class_var = np.insert(np.random.normal(10, .1, 3), 1,
                       np.random.normal(50, .1, 3))

df_array = np.vstack((input_var1, class_var)).T
df = pd.DataFrame(df_array, columns=['gfs_wind_spd', 'metar_wind_spd'])

input_vars = ['gfs_wind_spd']
class_var = 'metar_wind_spd'

type_vars = ['lin', 'lin']

tree = tree_planter(df, class_var, input_vars, type_vars)

tree_pprinter(tree)