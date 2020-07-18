import streamlit as st
import json

from tensorflow.keras.models import load_model
import pandas as pd

def get_user_input():
    """
    this function is used to get user input using sidebar slider and selectbox
    return type : pandas dataframe
    """

    GRE_Score = st.sidebar.slider('GRE Score', 260, 340, 315)
    TOEFL_Score = st.sidebar.slider('TOEFL Score', 0, 120, 100)
    University  = st.sidebar.slider('University Rating', 1, 5, 3)
    SOP  = st.sidebar.slider('Statement of Purpose Score', 1, 5, 3)
    LOR  = st.sidebar.slider('LOR Score', 1, 5, 3)
    CGPA = st.sidebar.slider('CGPA', 6.00, 10.00, 7.50)
    Research = st.sidebar.selectbox("Previous Research Experience",("Yes", "No"))

    if Research=="Yes":
        Research = 1
    else:
        Research = 0

    features = {'GRE Score': GRE_Score,
            'TOEFL Score': TOEFL_Score,
            'University Rating': University,
            'SOP': SOP,
            'LOR ': LOR,
            'CGPA': CGPA,
            'Research': Research,
            }
    data = pd.DataFrame(features,index=[0])

    return data

data = get_user_input()

model_h5 = load_model('admission.h5')

mean = {'GRE Score': 316.472,
 'TOEFL Score': 107.192,
 'University Rating': 3.114,
 'SOP': 3.374,
 'LOR ': 3.484,
 'CGPA': 8.576440000000003}

std = {'GRE Score': 11.295148372354694,
 'TOEFL Score': 6.081867659564522,
 'University Rating': 1.1435118007598137,
 'SOP': 0.9910036207566069,
 'LOR ': 0.9254495738978181,
 'CGPA': 0.6048128003332052}

for item in mean.keys():
    data[item] = (data[item] - mean[item])/(std[item])

result = int(model_h5.predict(data)[0]*100)
st.subheader(f'Chance of Admit: {result}%')
