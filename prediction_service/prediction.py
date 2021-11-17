import yaml
import json
import numpy as np
import joblib
import json

params_path = "params.yaml"
schema_path = "prediction_service\schema_in.json"

class NotInRange(Exception):
    def __init__(self, message="Values entered are not in expected range"):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message="Not in cols"):
        self.message = message
        super().__init__(self.message)


def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict([data]).tolist()[0]
    with open("prediction_service/labels.json","r") as f:
        labels = json.load(f)
    return labels[str(prediction)]


def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema

def validate_input(dict_request):
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()
        #if not (schema[col]["min"] <= float(dict_request[col][0]) <= schema[col]["max"]) :
        #    raise NotInRange
        if not (schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]) :
            raise NotInRange

    for col, val in dict_request.items():
        _validate_cols(col)
        _validate_values(col, val)
    
    return True

def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values()
        data = [float(data_) for data_ in data]
        #data = [list(map(float, data))]
        response = predict(data)
        
        return response

def api_response(dict_request):
    try:
        if validate_input(dict_request):
            #data = np.array([list(dict_request.values())])
            data = list(dict_request.values())
            response = predict(data)
            response = {"response": response}
            return response
    except NotInRange as e:
        response = {"the_exected_range": get_schema(), "response": str(e) }
        return response

    except NotInCols as e:
        response = {"the_exected_cols": get_schema().keys(), "response": str(e) }
        return response




