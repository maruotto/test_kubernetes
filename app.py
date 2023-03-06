import streamlit as st
import joblib
import pandas as pd
from PIL import Image
import streamlit as st
from bokeh.plotting import figure
import requests
import json


def plot(glucose_levels):
    time = ["t-14", "t-13", "t-12", "t-11", "t-10", "t-9", "t-8", "t-7",
            "t-6", "t-5", "t-4", "t-3", "t-2", "t-1", "t", "t+6"]
    p = figure(title='Prediction',
               x_axis_label='Glucose Level', y_axis_label='Time')
    p.line(time, glucose_levels, legend_label='Trend', line_width=2)
    st.bokeh_chart(p, use_container_width=True)


@st.cache(allow_output_mutation=True)
def load(scaler_path, model_path):
    sc = joblib.load(scaler_path)
    model = joblib.load(model_path)
    return sc, model


def inference(row, scaler, model, feat_cols):
    df = pd.DataFrame([row], columns=feat_cols)
    X = scaler.transform(df)
    features = pd.DataFrame(X, columns=feat_cols)
    return model.predict(features)


st.set_page_config(page_title="Glucose Predictor", layout="wide")
st.title("Glucose Prediction")
# image = Image.open('/Users/idamaruotto/Downloads/photo.png')
# st.sidebar.image(image, use_column_width=True)
patient = st.sidebar.selectbox("Patient:",
                               ('540', '544', '552', '559', '563', '567'), key="patient")
csv_upload = st.sidebar.file_uploader("Upload a csv file", type=["csv", "CSV"])
if __name__ == '__main__':
    # sc, model = load()
    # = read_csv(csv_upload)
    # prediction = inference(upload=csv_upload)
    d = pd.read_csv("/Users/idamaruotto/Downloads/DiabetesLSTM/Datasets/540/540-ws-testing(t+30).csv", sep=',',
                    header=0)
    d.drop("var1(t+6)", axis=1, inplace=True)
    data = json.dumps({"instances": d.to_numpy().tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post('https://glucose-prediction-540-predictor-default-kubeflow-user.example.com'
                                  , data=data, headers=headers)
    predictions = json.loads(json_response.text)['predictions']
    print(predictions)
