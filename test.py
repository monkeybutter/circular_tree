from util import tree_planter, tree_pprinter, tree_bound_checker
import time
import pandas as pd


df = pd.read_csv("/Users/pablo/Dropbox/Data for Tree/egll.csv")
cols = list(df.columns)
class_var = cols[0]
del cols[0]
input_vars = cols
type_vars = ['lin'] + ['lin' for var in input_vars]

time1 = time.time()
tree_classic = tree_planter(df, class_var, input_vars, type_vars, 'classic', 500, 0.5)
tree_pprinter(tree_classic)
print("Check bounds: {}".format(tree_bound_checker(tree_classic)))
time2 = time.time()
print("Classic function took {0:.2f} ms".format((time2-time1)*1000.0))


"""
from dataset_generator import create_simple_data2
df = create_simple_data2(500, 50)
df.columns = ['gfs_wind_dir', 'metar_wind_spd']

input_vars = ['gfs_wind_dir']
class_var = 'metar_wind_spd'
type_vars = ['lin', 'lin']

time1 = time.time()
tree_classic = tree_planter(df, class_var, input_vars, type_vars, 'classic', 50, 0.2)
tree_pprinter(tree_classic)
print("Check bounds: {}".format(tree_bound_checker(tree_classic)))
time2 = time.time()
print("Classic function took {0:.2f} ms".format((time2-time1)*1000.0))



time1 = time.time()
tree_subset = tree_planter(df, class_var, input_vars, type_vars, 'subset', 50, 0.2)
tree_pprinter(tree_subset)
time2 = time.time()
print("Subset function took {0:.2f} ms".format((time2-time1)*1000.0))
"""