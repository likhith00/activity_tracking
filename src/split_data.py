import os
import argparse
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from get_data import read_params
import pandas as pd
import numpy as np
import json


def split_data(config_path):
    config = read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    train_path = config["split_data"]["train_path"]
    test_path= config["split_data"]["test_path"]
    random_state= config["base"]["random_state"]
    split_ratio = config["split_data"]["test_size"]
    TARGET = config["base"]["target_col"]
    df = pd.read_csv(raw_data_path,sep=',')
    df = df.drop(columns=["_id"],axis=1)
    lc = LabelEncoder()
    df[TARGET] = lc.fit_transform(df[TARGET])
    labels_dict = dict(zip(list(map(int,list(lc.transform(lc.classes_)))),lc.classes_))
    

    with open("labels.json", "w") as outfile:
        json.dump(labels_dict, outfile)
    
    train,test = train_test_split(df,test_size = split_ratio,random_state=random_state)
    train.to_csv(train_path,index=False,sep=',')
    test.to_csv(test_path,index=False,sep=',')
    

if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config",default="params.yaml")
    parsed_args = args.parse_args()
    split_data(config_path= parsed_args.config)