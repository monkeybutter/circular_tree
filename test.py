from util import tree_planter, tree_pprinter, create_simple_data2
import numpy as np
import pandas as pd



df = create_simple_data2(1000, 50)
df.columns = ['gfs_wind_dir', 'metar_wind_spd']

input_vars = ['gfs_wind_dir']
class_var = 'metar_wind_spd'
type_vars = ['lin', 'lin']

tree = tree_planter(df, class_var, input_vars, type_vars, 50, 0.2)

tree_pprinter(tree)