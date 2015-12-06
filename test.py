from util import tree_planter, tree_pprinter
import numpy as np
import pandas as pd

# Test Subset Tree
input_var1 = np.arange(0, 360)

class_var = np.ones(360)

class_var[:40] = np.random.normal(1, .1, 40)
class_var[330:] = np.random.normal(1, .1, 30)
class_var[40:80] = np.random.normal(7, .1, 40)
class_var[80:120] = np.random.normal(10, .1, 40)
class_var[230:330] = np.random.normal(10, .1, 100)
class_var[120:230] = np.random.normal(20, .1, 110)

df_array = np.vstack((input_var1, class_var)).T
df = pd.DataFrame(df_array, columns=['gfs_wind_dir', 'metar_wind_spd'])

input_vars = ['gfs_wind_dir']
class_var = 'metar_wind_spd'
type_vars = ['cir', 'lin']

df = pd.DataFrame(df_array, columns=input_vars + [class_var])

tree = tree_planter(df, class_var, input_vars, type_vars)

tree_pprinter(tree)