class Data(object):
    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):  # , first=True):
        self.df = df.copy()
        # self.df.dropna(inplace=True)
        self.var_desc = var_desc
        self.class_var = class_var
        self.input_vars = list(self.var_desc.keys())


    def sort_by(self, col_name):

        self.df = self.df.sort_values(col_name)

        if self.var_desc[col_name]["type"] == 'cir':
            start = self.var_desc[col_name]["bounds"][0][0]
            end = self.var_desc[col_name]["bounds"][-1][1]

            if start > end:
                self.df = self.df.query('{} <= {} <= 360.0'.format(start, col_name)).copy().append(
                    self.df.query('0.0 <= {} < {}'.format(col_name, end)).copy())

        self.df.index = range(0, len(self.df.index))
