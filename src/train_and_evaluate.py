import os
import argparse
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from get_data import read_params
from sklearn.metrics import accuracy_score
import json
import joblib


def train_and_evaluate(config_path):
    config = read_params(config_path)
    train_path = config["split_data"]["train_path"]
    test_path = config["split_data"]["test_path"]
    train_data = pd.read_csv(train_path,sep=',')
    test_data = pd.read_csv(test_path,sep=',')
    neighbors = config["estimators"]["KNeighborsClassifier"]["params"]["n_neighbors"]
    target = [config["base"]["target_col"]]
    model_dir = config["model_dir"]
    X_train = train_data.drop(columns=target,axis=1)
    X_test = test_data.drop(columns=target,axis=1)
    y_train = train_data[target]
    y_test  = test_data[target]
    reports = config["reports"]["scores"]
    
    knc = KNeighborsClassifier(n_neighbors= neighbors)
    knc.fit(X_train,y_train)
    y_pred = knc.predict(X_test)
    score = accuracy_score(y_test,y_pred)
    score = {"accuracy":score}
    with open(reports,"w") as json_file:
        json.dump(score,json_file,indent=4)
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(knc,model_path)




if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config",default='params.yaml')
    parsed_args = args.parse_args()
    train_and_evaluate(config_path = parsed_args.config)