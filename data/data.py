class Data(object):
    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):  # , first=True):
        self.df = df.copy()
        # self.df.dropna(inplace=True)
        self.class_var = class_var
        self.var_desc = var_desc

    def sort_by(self, col_name):

        if self.var_desc[col_name]["type"] == 'lin':
            self.df = self.df.sort_values(col_name)
            self.df.index = range(0, len(self.df))

        elif self.var_desc[col_name]["type"] == 'cir':

            self.df = self.df.sort_values(col_name)

            start = self.var_desc[col_name]["bounds"][0][0]
            end = self.var_desc[col_name]["bounds"][-1][1]

            if start > end:
                self.df = self.df.query('{} < {} < 360.0'.format(start, col_name)).copy().append(
                    self.df.query('0.0 < {} < {}'.format(col_name, start)).copy())

            self.df.index = range(0, len(self.df))

        else:
            raise Exception("Variable type {} not recognised!".format(self.var_desc[col_name]["type"]))
