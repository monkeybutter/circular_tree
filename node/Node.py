import copy
import pandas as pd
from data.classic_data import ClassicData
from data.subset_data import SubsetData

class Node(object):
    __class_description__ = """Class modelling the actual structure of a binary tree node"""
    __version__ = 0.1

    def __init__(self, data, stop=500, level=0):
        self.split_var = None
        self.data = data
        self.level = level
        self.stop = stop
        self.left_child = None
        self.right_child = None
        
    def split(self):
        if len(self.data.df.index) > self.stop:
            split = self.data.get_best_split()
            self.split_var = split["var_name"]
            self.data.sort_by(self.split_var)

            if self.data.__class__.__name__ == "ClassicData":

                split_value = (self.data.df.iloc[split['index']-1][split["var_name"]] +
                               self.data.df.iloc[split['index']][split["var_name"]]) / 2.0

                left_desc = copy.deepcopy(self.data.var_desc)
                left_desc[split["var_name"]]["bounds"][0][1] = split_value
                self.left_child = Node(ClassicData(self.data.df.iloc[:split['index']],
                                                   self.data.class_var, left_desc), self.stop, self.level+1)
                self.left_child.split()

                right_desc = copy.deepcopy(self.data.var_desc)
                right_desc[split["var_name"]]["bounds"][0][0] = split_value
                self.right_child = Node(ClassicData(self.data.df.iloc[split['index']:],
                                                    self.data.class_var, right_desc), self.stop, self.level+1)
                self.right_child.split()

            elif self.data.__class__.__name__ == "SubsetData":

                split_value1 = (self.data.df.iloc[split['index'][0]-1][split["var_name"]] +
                               self.data.df.iloc[split['index'][0]][split["var_name"]]) / 2.0

                split_value2 = (self.data.df.iloc[split['index'][1]-1][split["var_name"]] +
                               self.data.df.iloc[split['index'][1]][split["var_name"]]) / 2.0

                left_desc = copy.deepcopy(self.data.var_desc)
                left_desc[split["var_name"]]["bounds"][0][0] = split_value1
                left_desc[split["var_name"]]["bounds"][0][1] = split_value2
                self.left_child = Node(SubsetData(self.data.df.iloc[split['index'][0]:split['index'][1]],
                                                  self.data.class_var, left_desc), self.stop, self.level+1)
                self.left_child.split()

                right_desc = copy.deepcopy(self.data.var_desc)
                right_desc[split["var_name"]]["bounds"][-1][1] = split_value1
                right_desc[split["var_name"]]["bounds"].append([None, None])
                right_desc[split["var_name"]]["bounds"][-1][0] = split_value2
                self.right_child = Node(SubsetData(pd.concat([self.data.df.iloc[:split['index'][0]],
                                                              self.data.df.iloc[split['index'][1]:]]),
                                                   self.data.class_var, right_desc), self.stop, self.level+1)
                self.right_child.split()

            else:
                raise Exception("Data class not recognised!")
