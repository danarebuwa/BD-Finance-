import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from plotly import graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np 
import altair as alt

data = pd.read_csv("data//coin_Cardano.csv")
x = np.array(data['High']).reshape(-1,1)
lr = LinearRegression()
lr.fit(x,np.array(data['Volume']))


#st.title("Bussdown Worldwide Budget Calculator")
#ßst.image("data//BD Logo.png", width = 500)
#nav = st.sidebar.radio("Navigation",["Home","Predictive Model","Contribute"])
#st.header("Introduction")
#st.text("This is an interactive web app to help approximate finances and budget spending")
#st.header("Financial Information")
nav = st.sidebar.radio("Navigation",["Home","Budget Predictor","Add Information"])
if nav == "Home":

    st.title("Bussdown Worldwide Budget Calculator")
    st.image("data//BD Logo.png", width = 500)
    st.header("Introduction")
    st.text("This is an interactive web app to help approximate finances and budget spending")
    st.header("Financial Information")
    if st.checkbox("Show Historical Data"):
        st.table(data)
    st.subheader("Revenue Breakdown")
    df = pd.DataFrame(data)
    plt.bar(df['Name'], df['Low'])
    plt.title('CRevenue to Avg Spend', fontsize=14)
    plt.xlabel('Revenue', fontsize=14)
    plt.ylabel('Expense', fontsize=14)
    plt.grid(True)
    plt.show()
    st.pyplot()

    st.subheader("Expense Breakdown")
    st.dataframe(df.sort_values('Close',
             ascending=False).reset_index(drop=True))

    st.vega_lite_chart(df, {
         'mark': {'type':'circle', 'tooltip': True},
         'encoding': {
             'x': {'field': 'Low', 'type': 'quantitative' },
             'y': {'field': 'High','type': 'quantitative' },
             'color': {'field': 'position', 'type': 'nominal'},
             'tooltip': [{"field": 'Name', 'type': 'nominal'}, {'field': 'Marketcap', 'type': 'quantitative'}, {'field': 'Volume', 'type': 'quantitative'}],
         },
         'width': 700,
         'height': 400,
    })    
    
    st.subheader("Prospective Growth Model")
    graph = st.selectbox("Select Graph Variation ",["Non-Interactive","Interactive"])

    val = st.slider("Filter data using years",0,4)
    data = data.loc[data["High"]>= val]
    if graph == "Non-Interactive":
        plt.figure(figsize = (10,5))
        plt.scatter(data["High"],data["Volume"])
        plt.ylim(0)
        plt.xlabel("High")
        plt.ylabel("Volume")
        plt.tight_layout()
        st.pyplot()
    if graph == "Interactive":
        layout =go.Layout(
            xaxis = dict(range=[0,1]),
            yaxis = dict(range =[0,2])
        )
        fig = go.Figure(data=go.Scatter(x=data["High"], y=data["Volume"], mode='markers'),layout = layout)
        st.plotly_chart(fig)

    


    #graph = st.selectbox("Select Graph Variation ",["Non-Interactive","Interactive"])  

#plt.figure(figsize = (10,5))
#data2 = pd.read_csv("data//coin_Cardano.csv")

if nav == "Budget Predictor":
    st.header("Approx Budget Spend")
    val2 = st.text_input("Enter Venue Location" )
    val = st.number_input("Enter Estimated number in attendance" )
    val3 = st.number_input("Enter Venue Capactiy" )
    val4 = st.number_input("Enter weeks to event")
    val = np.array(val).reshape(1,-1)
    pred =lr.predict(val)[0]

    if st.button("Predict"):
        st.success(f"Your estimated Budget is {round(pred)}")

if nav == "Add Information":
    st.header("Contribute to dataset")
    ex = st.selectbox("Enter Event Location",('London', 'Manchester', 'Surrey', 'Abuja'))
    dt = st.date_input("Enter Event Date")
    at = st.number_input("Venue Capacity")
    sal = st.number_input("Enter average ticket price")

    if st.button("submit"):
        to_add = {"High":[ex],"Volume":[sal]}
        to_add = pd.DataFrame(to_add)
        to_add.to_csv("data//BD_Data.csv",mode='a',header = False,index= False)
        st.success("Submitted")
