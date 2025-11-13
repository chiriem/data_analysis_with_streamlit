import streamlit as st
import pandas as pd
import numpy as np
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

@st.cache_data
def get_data():
    bell_df = pd.read_csv("./data/비상벨.csv", index_col=0)
    return bell_df

@st.cache_data
def my_map():
    bell_df = get_data()
    bell_df[["lat","lon"]] = bell_df[["WGS84위도","WGS84경도"]]
    m = folium.Map(location=[bell_df["lat"].mean(), bell_df["lon"].mean()], zoom_start=12, width=800)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in bell_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
        ).add_to(marker_cluster)
    folium.TileLayer('cartodbpositron').add_to(m)
    
    folium_static(m)

def run_bell_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([7, 3])
    row5, row6 = st.columns([4, 6])

    bell_df = get_data()

    for col in row1:
        tile = col.container(height=170, border=True)
        select_reigon = tile.multiselect(
            "자치구 선택",
            bell_df["구"].unique(),
            default=bell_df["구"].unique(), key="bell_reigon")

    for col in row2:
        tile = col.container(height=100, border=True)
        tile.slider("연도 선택", 2003, 2025, (2003, 2025), key="bell_year")

    with row3.container(height=400, border=True):
        st.write("FUCK YOU")
        # chart = alt.Chart().mark_line().encode().properties()
        # st.altair_chart(chart, use_container_width=True)

    with row4.container(height=400, border=True):
        st.write("FUCK YOU")

    with row5:
        my_map()
    row6.container(height=500, border=True).dataframe(bell_df[["설치연도","WGS84위도", "WGS84경도", "구"]], height=450)