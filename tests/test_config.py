import pytest
import logging 
import os
import joblib
from prediction_service.prediction import form_response,api_response, form_response
import prediction_service

input_data = {
    "incorrect_range": 
    {
    "orX":400,
    "orY": 180.0,
    "orZ":  88.0,
    "rX":  1,
    "rY":  12,
    "rZ": 0.999904,
    "accX":-4.5367,
    "accY":12.575,
    "accZ": -5.97593,
    "gX": 3.6584,
    "gY": 5.8955,
    "gZ": -1.8281,
    "mX": 8.8,
    "mY": 120.4,
    "mZ":-107.2,
    "lux":1233.0,  
    "soundLevel": -20.57
},

    "correct_range":
    {
    "orX":0.0,
    "orY": 169.0,
    "orZ":  88.0,
    "rX":  0.80416,
    "rY":  0.723168,
    "rZ": 0.999904,
    "accX":-4.5367,
    "accY":12.575,
    "accZ": -5.97593,
    "gX": 3.6584,
    "gY": 5.8955,
    "gZ": -1.8281,
    "mX": 8.8,
    "mY": 120.4,
    "mZ":-107.2,
    "lux":1233.0,  
    "soundLevel": -20.57
}

}

TARGET_range = [
    "AscendingStairs",
    "ClimbingDownStairs",
    "ClimbingUpStairs",
    "DescendingStairs",
    "Driving",
    "Jogging",
    "Lying",
    "MountainAscending",
   "MountainDescending",
    "Running",
    "Sitting",
     "Standing",
   "Walking"
]


def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    print(res)
    assert res in TARGET_range

def test_api_response_correct_range(data=input_data["correct_range"]):
    print('inside api')
    res = api_response(data)
    print(res['response'])

    assert res['response'] in TARGET_range

def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)

def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message

