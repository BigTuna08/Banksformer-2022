import numpy as np
import pickle
from math import sin, cos, pi
# from datetime import date
import os
# import pandas as pd


# # from .constants import *


# self.categorical_fields
# self.LOG_AMOUNT_SCALE
# self.TD_SCALE
# self.ATTR_SCALE
# self.START_DATE


# self.__setattr__(f"{field}_to_num".upper(), cat_to_num)
            
# self.__setattr__(f"num_to_{field}".upper(), 
#                 dict([(i, tc) for i, tc in enumerate(df[field].unique())]))

# self.__setattr__(f"n_{field}s", len(cat_to_num)) 




import calendar


class DataEncoder:
    
    def __init__(self, categorical_fields):
        self.categorical_fields = categorical_fields
    
    
    def fit_transform(self, df):

        
        ####    Dates    ####
        self.START_DATE = df["datetime"].min()
        
        iso = df["datetime"].dt.isocalendar()
        df["month"] = df["datetime"].dt.month
        df["day"] = df["datetime"].dt.day
        df["dow"] =  df["datetime"].dt.dayofweek
        df["year"] = df["datetime"].dt.year
        # dtme - days till month end
        df["dtme"] = df.datetime.apply(lambda dt: calendar.monthrange(dt.year, dt.month)[1] - dt.day)
        
        df["td"] = df[["account_id", "datetime"]].groupby("account_id").diff()
        df["td"] = df["td"].apply(lambda x: x.days)
        df["td"].fillna(0.0, inplace=True)
        
        
        
        ####    Continous    ####
        df["log_amount"] = np.log10(df["amount"]+1)
        self.LOG_AMOUNT_SCALE = df["log_amount"].std()
        df["log_amount_sc"] = df["log_amount"] / self.LOG_AMOUNT_SCALE
        
        self.TD_SCALE = df["td"].std()
        df["td_sc"] = df["td"] / self.TD_SCALE
        
        self.ATTR_SCALE = df["age"].std()
        df["age_sc"] = df["age"] / self.ATTR_SCALE
        
        
        
        
        ####    Categorical    ####
        for field in self.categorical_fields:
            
            field = field.replace("_num", "")
            cat_to_num = dict([(tc, i) for i, tc in enumerate(df[field].unique())])
            self.__setattr__(f"{field}_to_num".upper(), cat_to_num)
            
            self.__setattr__(f"num_to_{field}".upper(), 
                            dict([(i, tc) for i, tc in enumerate(df[field].unique())]))
            
        
            df[field + "_num"] = df[field].apply(lambda x: cat_to_num[x])
            
            self.__setattr__(f"n_{field}s", len(cat_to_num)) 
            
            # add '_' to nan and blank so they are always interpreted as strings
            df[field] = df[field].astype(str).apply(lambda x: "_" + x  if x in ["nan", ""]  else x)
            
            
    def get_n_cats(self, field):
        field = field.replace("_num", "")
        field = f"n_{field}s"
        return self.__getattribute__(field)
    

    def get_code_num(self, field, code):
        field = field.replace("_num", "")
        d = self.__getattribute__(f"{field}_to_num".upper())
        return d[code]

    

    def get_code_from_num(self, field, num):
        field = field.replace("_num", "")
        d = self.__getattribute__(f"num_to_{field}".upper())
        return d[num]

        
        

# def preprocess_df(df, catfields, ds_suffix = None):
#     de = DataEncoder(catfields)
#     de.fit_transform(df)
    
#     if ds_suffix == None:
#         print("No ds_suffix set. Using ds_suffix = 'default'. (ds_suffix is used for keeping track of different dataset versions)")
#         ds_suffix = 'default'
    
    
#     with open(f"stored_data/DataEncoder-{ds_suffix}.pickle", "wb") as f:
#         pickle.dump(de, f) 
#         print("Wrote encoding info to", f.name)
        
#     return de

        

def load_data_encoder():
    
    loc = f"stored_data/DataEncoder.pickle"
    if "DataEncoder.pickle" in os.listdir("stored_data/"):
        with open(loc, "rb") as f:
            return pickle.load(f) 
        
    else:
        raise Exception(f"Error - No DataEncoder exists at {loc} !")

  
def encode_time_value(val, max_val):
    return sin(2* pi * val/max_val), cos(2*pi * val/max_val)

def bulk_encode_time_value(val, max_val):
    x = np.sin(2* np.pi/max_val * val)
    y = np.cos(2*np.pi /max_val * val)
    return np.stack([x,y], axis=1)
        