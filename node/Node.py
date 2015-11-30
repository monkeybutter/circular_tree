import copy
import pandas as pd
from data.classic_data import ClassicData
from data.subset_data import SubsetData

class Node(object):
    __class_description__ = """Class modelling the actual structure of a binary tree node"""
    __version__ = 0.1

    def __init__(self, data, level=0):
        self.split_var = None
        self.data = data
        self.level = level
        self.stop = 500
        self.left_child = None
        self.right_child = None
        print(self.data.__name__)
        
    def split(self):
        if len(self.data.df.index) > self.stop:
            split = self.data.get_best_split()
            print("best split", split)
            self.split_var = split["var_name"]
            self.data.sort_by(self.split_var)

            """
            split_value = (self.data.df.iloc[split['index']-1][split["var_name"]] + 
                           self.data.df.iloc[split['index']][split["var_name"]]) / 2.0
            """

            split_value = (self.data.df.iloc[split['index'][0]-1][split["var_name"]] +
                           self.data.df.iloc[split['index'][0]][split["var_name"]]) / 2.0
            
            left_desc = copy.deepcopy(self.data.var_desc)
            left_desc[split["var_name"]]["bounds"][0][1] = split_value
            #self.left_child = Node(ClassicData(self.data.df.iloc[:split['index']], self.data.class_var, left_desc), self.level+1)
            self.left_child = Node(SubsetData(self.data.df.iloc[split['index'][0]:split['index'][1]], self.data.class_var, left_desc), self.level+1)
            self.left_child.split()

            right_desc = copy.deepcopy(self.data.var_desc)
            right_desc[split["var_name"]]["bounds"][0][0] = split_value
            #self.right_child = Node(ClassicData(self.data.df.iloc[split['index']:], self.data.class_var, right_desc), self.level+1)
            self.right_child = Node(SubsetData(pd.concat([self.data.df.iloc[:split['index'][0]],
                                                          self.data.df.iloc[split['index'][1]:]]),
                                               self.data.class_var, right_desc), self.level+1)
            self.right_child.split()
