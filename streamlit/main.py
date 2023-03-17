import pandas as pd
from PIL import Image
import streamlit as st
import json
import requests
import numpy as np
from bokeh.plotting import figure

def plot(glucose_levels, time):
    time_data = pd.DataFrame(time, columns=['time'])
    data = pd.DataFrame(glucose_levels, columns=['glucose'])
    frames = [data, time_data]
    chart_data = pd.concat(frames,axis=1, join='inner')
    print(chart_data)
    st.line_chart(data = chart_data, x='time', y = 'glucose')
    #p = figure(
    #    title='Glucose Prediction',
    #    x_axis_label='Time',
    #    y_axis_label='Glucose')
    #list = []
    #for i in range(0, glucose_levels.shape[0]):
    #    list.append(glucose_levels[i])

    #p.line(time, list, legend_label='Glucose Level', line_width=5)
    #st.bokeh_chart(p, use_container_width=True)

def define_time(length):
    time = []
    for i in range(5,length):
        time.append(i+1)
    return time

def inference(data):
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://localhost:28015/v1/models/glucose_predictor:predict', data=data, headers=headers)
    predictions = np.array(json.loads(json_response.text)['predictions'])
    return predictions

def inference(data, patient):
    headers = {"content-type": "application/json"}
    #json_response = requests.post('http://localhost:'+patient+'0/v1/models/' + patient + ':predict', data=data, headers=headers)
    json_response = requests.post('http://glucose-prediction.info/' + patient + '/v1/models/' + patient + ':predict', data=data,
                                  headers=headers)
    print(json_response)
    predictions = np.array(json.loads(json_response.text)['predictions'])
    return predictions

def read_csv(csv_upload):
    d = pd.read_csv(csv_upload, sep=',', header=0)
    length = d.shape[0]
    d.drop("var1(t+6)", axis=1, inplace=True)
    data = json.dumps({"instances": d.to_numpy().tolist()})
    return data, length


st.set_page_config(page_title="Glucose Predictor", layout="wide")
st.title("Glucose Prediction")
image = Image.open('photoheader.png')
st.image(image, use_column_width=True)
image = Image.open('photo.jpg')
st.sidebar.image(image, use_column_width=True)
patient = st.sidebar.selectbox("Patient:",('540','544','552', '559', '563', '567'), key="patient")
csv_upload = st.sidebar.file_uploader("Upload a csv file", type=["csv", "CSV"])

if csv_upload is not None:
    data, length = read_csv(csv_upload)
    predictions = inference(data, patient)
    plot(predictions, define_time(length))