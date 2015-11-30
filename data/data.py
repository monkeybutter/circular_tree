class Data(object):

    __class_description__ = """Class modelling Data a Binary Tree based on Pandas DataFrame"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_desc):#, first=True):
        self.df = df.copy()
        #self.df.dropna(inplace=True)
        self.class_var = class_var
        self.var_desc = var_desc
