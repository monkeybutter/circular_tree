
from data.data import Data
from data.util import get_score

import sys

class ClassicData(Data):

    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):#, first=True):
        Data.__init__(self, df, class_var, var_desc)
        self.iter_i = 0
        
    def __iter__(self):
        self.iter_i = 0
        return self
    
    def __next__(self):
        if self.iter_i == len(self.df.index)-1:
            raise StopIteration
        else:
            self.iter_i += 1
            return (self.iter_i, self.df.iloc[:self.iter_i][self.class_var].values,
                    self.df.iloc[self.iter_i:][self.class_var].values)
        
    def get_best_split(self):
        best_split = {'var_name': None, 'score': 0.0, 'index': 0}

        iteration = 0
        for input_var in list(self.var_desc.keys()):

            #self.sort_by(input_var)

            self.df.sort_values(input_var, inplace=True)
            self.df.index = range(0, len(self.df.index))

            if input_var == 'gfs_wind_spd':
                print(self.df['metar_wind_spd'][234:244])


            for (i, left, right) in self:
                score = get_score(left, right)
                if score > best_split['score']:
                    iteration += 1
                    best_split.update({'var_name': input_var, 'score': score, 'index': i})

        print(iteration, best_split)

        sys.exit()

        return best_split
