import streamlit as st
from graphData import Data

st.header("METHANE: The Story Behind Climate CH3nge")

st.divider()


st.subheader("WELCOME!")
st.write("""This website serves as an interactive story: the story of Methane. What is it? Why should I care about it? 
         Well, with the help of NASA, this story presents itself in a non-traditional format to hopefully reach a greater interest and a call for action. 
         Get on to explore!""")

st.divider()

import pandas as pd
import io

st.subheader("Methane: The alarming greenhouse gas that is in the rise!")

def text_to_dataframe(text, delimiter= "      "):
    return pd.read_csv(io.StringIO(text), delim_whitespace=True)


df = text_to_dataframe(Data)

x_min = 1982
x_max = 2025 

y_min = 1600  
y_max = 1950

filtered_df = df[(df['year'] >= x_min) & (df['year'] <= x_max)]


import plotly.graph_objects as go

fig = go.Figure()

# Add a trace for the average values
fig.add_trace(go.Scatter(
    x=filtered_df['year'],
    y=filtered_df['average'],
    mode='lines+markers',
    name='Average',
    line=dict(shape='linear', color="#661c1c")
))

# Update layout to set x-axis limits
fig.update_layout(
    #title='Average Values Over Years',
    xaxis_title='Year',
    yaxis_title='CH₄ (parts per billion)',
    xaxis=dict(range=[x_min, x_max], gridcolor='lightgray'), 
    yaxis=dict(range=[y_min, y_max]),
    height=400
)

st.plotly_chart(fig)
st.write("Source: (NASA, 2024)")

st.divider()
st.subheader("Pages")

A, B, C, E = st.columns(4)
A.page_link("pages/01_🌍_Maps.py", label="Maps", icon="🌍")
B.page_link("pages/02_☀️_Things to Know.py", label="Things to Know", icon="☀️")
C.page_link("pages/03_📝_Data.py", label="Data", icon="📝")
E.page_link("pages/05_⚠️_Disclaimer.py", label="Disclaimer", icon="⚠️")
