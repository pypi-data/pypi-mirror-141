
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

def Label(data,col=None):
    """convert categorical values to numbers
    :data: Dataframe needed to processed
    :col: categorical columns to be converted to numbers,if None all columns with object datatype will be labelled"""

    c = LabelEncoder()
    l=[]
    if col==None:
        for i in data.columns:
            if str(data[i].dtype) == 'object':
                l.append(i)
        col = l


    for i in col:
        data[i] = c.fit_transform(data[i])

    return data

#print(Labelling(pd.DataFrame({'a':['a','b'],'b':['s','s']})))
