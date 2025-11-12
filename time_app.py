import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import os
import matplotlib.font_manager as fm # 한글 폰트 관련 용도
import folium
import geopandas as gpd
import json
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import time
from vega_datasets import data

@st.cache_data
def get_crime():
    crime = pd.read_excel("./data/seoul_crime.xlsx", index_col=0)
    return crime

def run_time_app():
    df = get_crime()
    crime_time = df.iloc[:, 1:9].sum(axis=0)
    c_df = crime_time.to_frame(name="범죄 발생 횟수")
    c_df.reset_index(inplace=True)
    c_df = c_df.rename(columns={"index":"Time"})

    row1, row2 = st.columns([7,3])
    # row1.container(height=400, border=True).bar_chart(c_df, x=None, y="범죄 발생 횟수", color="#ffaa00")
    chart = alt.Chart(c_df).mark_bar(color="red").encode(
        x="Time", y="범죄 발생 횟수",
    ).properties(title=alt.Title(text="시간대별 범죄 발생 횟수", align="center", anchor="middle"))
    row1.container(height=400, border=True).altair_chart(chart)