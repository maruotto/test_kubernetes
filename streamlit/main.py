import pandas as pd
from PIL import Image
import streamlit as st
import json
import requests
import numpy as np

def plot(glucose_levels):
    time = ["t-14", "t-13","t-12","t-11", "t-10", "t-9", "t-8", "t-7",
            "t-6","t-5","t-4", "t-3", "t-2","t-1","t","t+6"]
    chart_data = pd.DataFrame(glucose_levels, columns=['glucose'])
    st.line_chart(data = chart_data)

def inference(data):
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://localhost:28015/v1/models/glucose_predictor:predict', data=data, headers=headers)
    predictions = np.array(json.loads(json_response.text)['predictions'])
    return predictions

def inference(data, patient):
    headers = {"content-type": "application/json"}
    #json_response = requests.post('http://localhost:'+patient+'0/v1/models/' + patient + ':predict', data=data, headers=headers)
    json_response = requests.post('http://glucose-predictor.info/' + patient + '/v1/models/' + patient + ':predict', data=data,
                                  headers=headers)
    print(json_response)
    predictions = np.array(json.loads(json_response.text)['predictions'])
    return predictions

def read_csv(csv_upload):
    d = pd.read_csv(csv_upload, sep=',', header=0)
    d.drop("var1(t+6)", axis=1, inplace=True)
    data = json.dumps({"instances": d.to_numpy().tolist()})
    return data


st.set_page_config(page_title="Glucose Predictor", layout="wide")
st.title("Glucose Prediction")
image = Image.open('photoheader.png')
st.image(image, use_column_width=True)
image = Image.open('photo.jpg')
st.sidebar.image(image, use_column_width=True)
patient = st.sidebar.selectbox("Patient:",('540','544','552', '559', '563', '567'), key="patient")
csv_upload = st.sidebar.file_uploader("Upload a csv file", type=["csv", "CSV"])

if csv_upload is not None:
    data = read_csv(csv_upload)
    predictions = inference(data, patient)
    #predictions = inference(data)
    plot(predictions)