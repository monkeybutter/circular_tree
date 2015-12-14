import numpy as np
from data.util import get_score
from data.data import Data

class SubsetData(Data):

    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):#, first=True):
        Data.__init__(self, df, class_var, var_desc)
        self.iter_i = [0, 0]
        self.iter_var = 0

    def __iter__(self):
        self.iter_i = [0, 0]
        self.iter_var = 0
        self.sort_by(self.input_vars[self.iter_var])
        self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                 self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1

        return self
    
    def __next__(self):

        found = False

        while not found:

            self.iter_i[1] += 1

            if self.iter_i[1] == len(self.iter_idx):
                if self.iter_i[0] == len(self.iter_idx)-1:
                    if self.iter_var == len(self.input_vars)-1:
                        raise StopIteration
                    else:
                        self.iter_var += 1
                        self.sort_by(self.input_vars[self.iter_var])
                        self.iter_i = [0, 0]
                        self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                                 self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1
                else:
                    self.iter_i[0] += 1
                    self.iter_i[1] = self.iter_i[0]
                    self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                             self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1

            else:
                found = True

        return (self.iter_var, [self.iter_idx[self.iter_i[0]], self.iter_idx[self.iter_i[1]]],
                self.df.iloc[self.iter_idx[self.iter_i[0]]:self.iter_idx[self.iter_i[1]]][self.class_var].values,
                np.concatenate((self.df.iloc[:self.iter_idx[self.iter_i[0]]][self.class_var].values,
                                self.df.iloc[self.iter_idx[self.iter_i[1]]:][self.class_var].values)))


    def get_best_split(self):
        best_split = {'var_name': None, 'score': 0.0, 'index': [0, 0]}

        for input_var in list(self.var_desc.keys()):
            self.sort_by(input_var)
            for (var_i, i, left, right) in self:
                score = get_score(left, right)
                if score > best_split['score']:
                    best_split.update({'var_name': self.input_vars[var_i], 'score': score, 'index': i[:]})

        return best_split
