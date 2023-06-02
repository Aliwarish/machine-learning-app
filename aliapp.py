import streamlit as st
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"]{{
background-image: url("https://user-images.githubusercontent.com/112406455/219126717-b00f77f9-f3f2-44f2-86ef-bbadebe6b0de.png");
backgroung-size: cover;
}}

[data-testid="stHeader"]{{
   background-color:#0523a8;
}}
[data-testid="stSidebar"]{{
   color:#db1665;
   }}
   
 .sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}

[data-testid="stMarkdown"]{{
    color:#0c0c0d;
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as plt
import os

import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

import pycaret
from pycaret.classification import setup, compare_models, pull, save_model, ClassificationExperiment
from pycaret.regression import setup, compare_models, pull, save_model, RegressionExperiment
import base64

st.image("https://englishtribuneimages.blob.core.windows.net/gallary-content/2022/3/2022_3$largeimg_1263359305.jpg")
st.title("Machine Learning App")

if os.path.exists("sourcev.csv"):
    df = pd.read_csv("sourcev.csv",index_col=None)

with st.sidebar:
    st.header("Welcome to Machine Learning Application!")
    st.info("Select the options to work on the dataset. The uploded dataset can be analysed by using 'Explore' button. To train the model, choose the area you want to work on i.e., Classification & Regression. You can download the model (.pkl) file using 'Download' button. ")
    st.caption("Choose your parameters here: ")
    choose=st.radio(":computer:",["Dataset","Explore","Train","Download"])
    
if choose=="Dataset":
    st.write("Please upload your dataset here. Only .csv files allowed :smiley:")
    dataset_value = st.file_uploader("Upload here")
    
    if dataset_value:
        df = pd.read_csv(dataset_value, index_col=None)
        df.to_csv("sourcev.csv", index = None)
        st.dataframe(df)

if choose=="Explore":
    st.subheader("Perform profiling on Dataset")
    if st.sidebar.button("Do Analysis"):
        profile_report = df.profile_report() 
        st_profile_report(profile_report)
    
if choose=="Train":
    st.header("Start Training your Model now.")
    choice = st.sidebar.selectbox("Select your Technique:", ["Classification","Regression"])
    target = st.selectbox("Select you Target Variable",df.columns)
    if choice=="Classification":
        if st.sidebar.button("Classification Train"):
            s1 = ClassificationExperiment()
            s1.setup(data=df, target=target)
            setup_df = s1.pull()
            st.info("The Setup data is as follows:")
            st.table(setup_df)
            
            best_model1 = s1.compare_models()
            compare_model = s1.pull()
            st.info("The Comparison of models is as folows:")
            st.table(compare_model)
            
            best_model1
            s1.save_model(best_model1,"Machine Learning Model")
    else:
        if st.sidebar.button("Regression Train"):
            s2 = RegressionExperiment()
            s2.setup(data=df, target=target)
            setup_df = s2.pull()
            st.info("The Setup data is as follows:")
            st.table(setup_df)
            
            best_model2 = s2.compare_models()
            compare_model = s2.pull()
            st.info("The Comparison of models is as folows:")
            st.table(compare_model)
            
            best_model2
            s2.save_model(best_model2,"Machine Learning Model")

if choose =="Download":
    with open("Machine Learning model.pkl",'rb') as f:
        st.caption("Download your model from here:")
        st.download_button("Download the file",f,"Machine Learning model.pkl")
        
    
    
