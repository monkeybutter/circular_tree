import numpy as np
from data.util import get_score
import sys

class Data(object):
    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):  # , first=True):
        self.df = df.copy()
        # self.df.dropna(inplace=True)

        # Dict with the info of input variables
        self.var_desc = var_desc
        self.class_var = class_var

        # This is here because we need a persistent way of traversing the variables (for the iterators)
        self.input_vars = list(self.var_desc.keys())

        self.iter_i = [None, None]
        self.iter_var = None
        self.iter_idx = [None]

    def sort_by(self, col_name):
        self.df = self.df.sort_values(col_name)

        if self.var_desc[col_name]["type"] == 'cir':
            start = self.var_desc[col_name]["bounds"][0][0]
            end = self.var_desc[col_name]["bounds"][-1][1]

            if start > end:
                self.df = self.df.query('{} <= {} <= 360.0'.format(start, col_name)).copy().append(
                    self.df.query('0.0 <= {} < {}'.format(col_name, end)).copy())

        self.df.index = range(0, len(self.df.index))

    def __iter__(self):

        self.iter_var = 0

        if self.var_desc[self.input_vars[self.iter_var]]["method"] == "classic":
            if self.var_desc[self.input_vars[self.iter_var]]["type"] == "cir" and self.var_desc[self.input_vars[self.iter_var]]["bounds"] == [[-np.inf, np.inf]]:
                self.iter_i = [0, 0]
            else:
                self.iter_i = [None, 0]
        elif self.var_desc[self.input_vars[self.iter_var]]["method"] == "subset":
            self.iter_i = [0, 0]
        else:
            raise Exception("Method not recognised.")

        self.sort_by(self.input_vars[self.iter_var])
        self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                 self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1

        return self

    def __next__(self):
        found = False

        while not found:
            self.iter_i[1] += 1

            # == modified to >=
            # if sequence is all constant self.iter_i[1] == 1 doesn't match len(self.iter_idx) == 0
            if self.iter_i[1] >= len(self.iter_idx):
                if self.iter_i[0] is None or self.iter_i[0] >= len(self.iter_idx)-1:
                    if self.iter_var < len(self.input_vars):
                        self.iter_var += 1
                        if self.iter_var == len(self.input_vars):
                            raise StopIteration
                        else:
                            if self.var_desc[self.input_vars[self.iter_var]]["method"] == "classic":

                                if self.var_desc[self.input_vars[self.iter_var]]["type"] == "cir" and self.var_desc[self.input_vars[self.iter_var]]["bounds"] == [[-np.inf, np.inf]]:
                                    self.iter_i = [0, 0]
                                else:
                                    self.iter_i = [None, 0]
                            elif self.var_desc[self.input_vars[self.iter_var]]["method"] == "subset":
                                self.iter_i = [0, 0]
                            self.sort_by(self.input_vars[self.iter_var])
                            self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                                     self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1
                else:
                    self.iter_i[0] += 1
                    self.iter_i[1] = self.iter_i[0]
                    self.iter_idx = np.where(self.df[self.input_vars[self.iter_var]].values[:-1] !=
                                             self.df[self.input_vars[self.iter_var]].values[1:])[0] + 1

            else:
                found = True

        if self.iter_i[0] is None:
            return (self.iter_var, [None, self.iter_idx[self.iter_i[1]]],
                    self.df.iloc[:self.iter_idx[self.iter_i[1]]][self.class_var].values,
                    self.df.iloc[self.iter_idx[self.iter_i[1]]:][self.class_var].values)
        else:
            return (self.iter_var, [self.iter_idx[self.iter_i[0]], self.iter_idx[self.iter_i[1]]],
                    self.df.iloc[self.iter_idx[self.iter_i[0]]:self.iter_idx[self.iter_i[1]]][self.class_var].values,
                    np.concatenate((self.df.iloc[:self.iter_idx[self.iter_i[0]]][self.class_var].values,
                                    self.df.iloc[self.iter_idx[self.iter_i[1]]:][self.class_var].values)))

    def get_best_split(self):
        best_split = {'var_name': None, 'score': 0.0, 'index': [None, 0]}

        for (var_i, i, left, right) in self:
            score = get_score(left, right)
            if score > best_split['score']:
                best_split.update({'var_name': self.input_vars[var_i], 'score': score, 'index': i[:]})

        """ Tracking nodes
        if len(self.df.index) == 2925:

        """

        return best_split
