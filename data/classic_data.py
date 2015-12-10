
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
        
    def __iter__(self):
        self.iter_i = 0
        self.iter_var = 0
        self.sort_by(self.input_vars[self.iter_var])

        return self
    
    def __next__(self):

        ### Get this right, ponlo bonito Pablo!


        # 1.- Look for next different
        current_value = self.df.iloc[self.iter_i][self.input_vars[self.iter_var]]

        while current_value == self.df.iloc[self.iter_i][self.input_vars[self.iter_var]] and self.iter_i < len(self.df.index)-1:
            self.iter_i += 1

        if self.iter_i == len(self.df.index)-1:
            self.iter_i = 0
            if self.iter_var == len(self.input_vars)-1:
                raise StopIteration
            else:
                self.iter_var += 1
                self.sort_by(self.input_vars[self.iter_var])
                current_value = self.df.iloc[self.iter_i][self.input_vars[self.iter_var]]

        while current_value == self.df.iloc[self.iter_i][self.input_vars[self.iter_var]] and self.iter_i < len(self.df.index)-1:
            self.iter_i += 1

        return (self.iter_var, self.iter_i, self.df.iloc[:self.iter_i][self.class_var].values,
                self.df.iloc[self.iter_i:][self.class_var].values)


    def get_best_split(self):
        best_split = {'var_name': None, 'score': 0.0, 'index': 0}

        for (var_i, i, left, right) in self:
            #print(var_i, i)
            #sys.exit()
            score = get_score(left, right)
            if score > best_split['score']:
                best_split.update({'var_name': self.input_vars[var_i], 'score': score, 'index': i})

        return best_split
