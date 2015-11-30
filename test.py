from util import tree_planter, tree_pprinter
import numpy as np
import pandas as pd

a = np.ones(1800)*4

input_var1 = np.concatenate((np.random.uniform(3, 5, 800), np.random.uniform(7, 9, 700)), axis=0)
class_var = np.concatenate((np.random.uniform(3, 5, 800)*2, np.random.uniform(7, 9, 700)*2), axis=0)

df_array = np.vstack((input_var1, class_var)).T
df = pd.DataFrame(df_array, columns=['gfs_wind_spd', 'metar_wind_spd'])

input_vars = ['gfs_wind_spd']
class_var = 'metar_wind_spd'

type_vars = ['lin', 'lin']

tree = tree_planter(df, class_var, input_vars, type_vars)

tree_pprinter(tree)