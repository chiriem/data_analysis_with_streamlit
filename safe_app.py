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
def get_safe():
    safe = pd.read_csv("./data/safe_wgs84.csv")
    safe = safe[safe['latitude'].notnull()]
    return safe

@st.cache_data
def my_map():
    safe = get_safe()

    m = folium.Map(location=[safe["latitude"].mean(), safe["longitude"].mean()], zoom_start=12, width=800)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in safe.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
        ).add_to(marker_cluster)
    folium.TileLayer('cartodbpositron').add_to(m)
    # st_data = st_folium(m, width=500, height=500)
    folium_static(m)

def run_safe_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([7, 3])
    row5, row6 = st.columns([4, 6])

    safe = get_safe()

    for col in row1:
        tile = col.container(height=100, border=True)
        tile.multiselect(
            "자치구 선택",
            ["강남구", "마포구", "서초구", "서대문구"],
            default=["서대문구"], key="safe_reigon")

    for col in row2:
        tile = col.container(height=100, border=True)
        tile.slider("연도 선택", 2011, 2025, (2011, 2025), key="safe_year")

    source = data.barley()

    row3.container(height=400, border=True).bar_chart(source, x="variety", y="yield", color="site", horizontal=True)
    row4.container(height=400, border=True).title("Analysis Result")

    with row5:
        my_map()
    row6.container(height=500, border=True).dataframe(safe[["자치구", "브랜드", "소재지"]], height=450)