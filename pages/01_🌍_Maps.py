import webbrowser
import streamlit as st
from dates import makeMap
from streamlit_folium import st_folium


st.header("🌍 Maps")

st.write("In this section you can build your own customizable maps! Build from data provided by NASA, these constructions model GOSAT-based Top-down Total and Natural Methane Emissions. Personalize them and see how, when moving more in time to the present, the color intensity and new places where it appears increases. Keep exploring the website to learn more about these data.")

with st.expander("Date"):
    st.write('''
        This sample of data
    ''')

    if 'year' not in st.session_state:
        st.session_state.year = 1999  

    if 'month' not in st.session_state:
        st.session_state.month = 1 

    st.session_state.year = st.selectbox('Select Year', options=range(1999, 2025),key='year_selectbox')
    st.session_state.month = st.selectbox('Select Month', options=[f"{m:02d}" for m in range(1, 13)], key='month_selectbox')

st.session_state.transparency = st.slider("Transparency", min_value=0.0, max_value=1.0, step=0.1)



with st.expander("Color"):
    st.write('''
        This sample of data
    ''')

    if 'color' not in st.session_state:
        st.session_state.color = "twilight"

    st.session_state.color = st.selectbox('Select Color', options=['viridis', 'plasma', 'inferno', 'magma', 'cividis','twilight', 'twilight_shifted', 'hsv'],key='color_selectbox')

st.write(st.session_state.color)

mapButton = st.button("Make Map!")

st.write(st.session_state.transparency)

if mapButton:
    newMap = makeMap(st.session_state.year, st.session_state.month, st.session_state.transparency,st.session_state.color)
    if newMap:
        webbrowser.open(newMap, new=2)
    else:
        st.write("no map found")
