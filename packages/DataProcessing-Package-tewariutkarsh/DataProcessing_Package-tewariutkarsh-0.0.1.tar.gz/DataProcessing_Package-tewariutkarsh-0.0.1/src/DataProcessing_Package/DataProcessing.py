from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport


class PreProcess:

    def __init__(self, data):
        self.data = data
        self.check()


    def check(self):
        if(self.checkDF()==True or self.checkNumArr()==True):
            self.DF()
        else:
            raise "Expected a 2D numpy array or a DataFrame"


    def __checkT(self, df):
        if(type(df)==type(pd.DataFrame())):
            return True

        elif(type(df)==type(np.array()) and df.ndim>1):
            return True

        else:
            return False

    def StandardScalar(self, d_std):
        if(self.__checkT(d_std)==True):
            scaler = StandardScaler()
            scaler.fit_transform(self.data)
            return scaler.transform(d_std)

        else:
            raise f"Expected a 2D numpy array or a DataFrame for d_std input"

    def Report(self):
        if (self.checkDF()):
            return ProfileReport(self.data)

        elif (self.checkNumArr()):
            return ProfileReport(pd.DataFrame(self.data))

        else:
            raise f"Expected a 2D numpy array or a DataFrame"

    def Describe(self):
        if (self.checkDF()):
            return self.data.describe()

        elif (self.checkNumArr()):
            return pd.DataFrame(self.data).describe()

        else:
            raise f"Expected a 2D numpy array or a DataFrame"

    def Info(self):
        if(self.checkDF()):
            return self.data.info()

        elif(self.checkNumArr()):
            return pd.DataFrame(self.data).info()

        else:
            raise f"Expected a 2D numpy array or a DataFrame"

    def DF(self):
        if(self.checkNumArr()):
            return pd.DataFrame(self.data)

        elif(self.checkDF()):
            return self.data

        else:
            raise f"Expected a 2D numpy array or a DataFrame"


    def checkDF(self, d=pd.DataFrame()):
        if(type(self.data) == type(pd.DataFrame())):
            return True

        return False

    def checkNumArr(self, d=pd.DataFrame()):
        if(type(self.data) == type(np.array())):
            if(self.data.ndim > 1):
                return True
            else:
                return False
        return False