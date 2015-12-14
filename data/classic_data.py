import numpy as np
from data.data import Data
from data.util import get_score

import sys

class ClassicData(Data):

    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):#, first=True):
        Data.__init__(self, df, class_var, var_desc)
        self.iter_i = 0
        self.iter_var = 0
        self.iter_idx = []
        
    def __iter__(self):

        self.iter_i = -1
        self.iter_var = 0
        self.sort_by(self.input_vars[self.iter_var])
        self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                 self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1

        return self
    
    def __next__(self):

        #Objective: Find next split candidate
            # 1.- Can be in same df column
            # 2.- Can be in other column
            # 3.- Current one can be the last one

        found = False

        while not found:

            self.iter_i += 1

            if self.iter_i == len(self.iter_idx):
                if self.iter_var == len(self.input_vars)-1:
                    raise StopIteration
                else:
                    self.iter_i = -1
                    self.iter_var += 1
                    self.sort_by(self.input_vars[self.iter_var])
                    self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                             self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1

            else:
                found = True

        return (self.iter_var, self.iter_idx[self.iter_i],
                self.df.iloc[:self.iter_idx[self.iter_i]][self.class_var].values,
                self.df.iloc[self.iter_idx[self.iter_i]:][self.class_var].values)

    def get_best_split(self):
        best_split = {'var_name': None, 'score': 0.0, 'index': 0}

        for (var_i, i, left, right) in self:
            score = get_score(left, right)
            if score > best_split['score']:
                best_split.update({'var_name': self.input_vars[var_i], 'score': score, 'index': i})

        return best_split
