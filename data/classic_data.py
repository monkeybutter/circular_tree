
from data.data import Data
from data.util import get_score

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
        
    def sort_by(self, col_name):
        self.df = self.df.sort_values(col_name)
        self.df.index = range(0, len(self.df))
        
    def get_best_split(self):
        best_split = {'var_name': None, 'score': 0.0, 'index': 0}

        for input_var in list(self.var_desc.keys()):
            self.sort_by(input_var)
            for (i, left, right) in self:
                print(i)
                score = get_score(left, right)
                if score > best_split['score']:
                    best_split.update({'var_name': input_var, 'score': score, 'index': i})

        return best_split
