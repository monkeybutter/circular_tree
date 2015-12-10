
from data.data import Data
from data.util import get_score

class ClassicData(Data):

    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):#, first=True):
        Data.__init__(self, df, class_var, var_desc)
        self.iter_i = 0
        self.iter_var = 0
        
    def __iter__(self):
        self.iter_var = 0

        return self
    
    def __next__(self):

        """
        prev_val = self.df.iloc[self.iter_i][pred_var]

        for index in range(1, data.df.shape[0]-1):
            if prev_val != data.df[pred_var].iloc[index]:
        """

        ### Get this right, never starts at the end of sequence!

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


    # Iterator has to give next different value! Splits within values are missleading for bound checking!...
    def get_best_split(self):
        best_split = {'var_name': None, 'score': 0.0, 'index': 0}

        for (var_i, i, left, right) in self:
            score = get_score(left, right)
            if score > best_split['score']:
                best_split.update({'var_name': self.input_vars[var_i], 'score': score, 'index': i})

        return best_split
