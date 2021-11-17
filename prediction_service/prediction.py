import yaml
import json
import numpy as np
import joblib

params_path = "params.yaml"


def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    print("IN PREDICT",data)
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict([data]).tolist()[0]
    print(prediction)
    return prediction

def form_response(dict_request):
    data = dict_request.values()
    print(data)
    data = [float(data_[0]) for data_ in data]
    #data = [list(map(float, data))]
    print(data)
    response = predict(data)
    return response

def api_response(dict_request):
    try:
        data = np.array([list(dict_request.values())])
        response = predict(data)
        response = {"response": response}
        return response
    except Exception as e:
        response = {"response": str(e) }
        return response
