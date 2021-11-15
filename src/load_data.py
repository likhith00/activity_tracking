import argparse
import os
import pandas as pd
import argparse
from get_data import get_data,read_params

def load_data(config_path):
    config= read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    df = get_data(config_path)
    print(df.columns)
    df.to_csv(raw_data_path,sep=',',index=False,header=df.columns)
    

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config",default="params.yaml")
    parsed_args = args.parse_args()
    load_data(config_path=parsed_args.config)