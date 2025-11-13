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
import scipy.stats as stats

@st.cache_data
def get_enter():
    enter = pd.read_csv("./data/유흥업소_최종.csv")
    return enter

@st.cache_data
def get_enter_crime():
    enter_crime = pd.read_csv("./data/업소_찐막.csv")
    return enter_crime

@st.cache_data
def enter_map():
    enter = get_enter()
    m = folium.Map(location=[enter["latitude"].mean(), enter["longitude"].mean()], zoom_start=12, width=800)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in enter.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
        ).add_to(marker_cluster)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium_static(m)

@st.cache_data
def pearson():
    enter_crime = get_enter_crime()
    corr = stats.pearsonr(enter_crime["업소 갯수"], enter_crime["범죄수"])
    return corr

def run_enter_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([7, 3])
    row5, row6 = st.columns([4, 6])

    enter = get_enter()
    enter_crime = get_enter_crime()
    corr = pearson()

    for col in row1:
        tile = col.container(height=170, border=True)
        select_reigon = tile.multiselect(
            "자치구 선택",
            enter["구"].unique(),
            default=enter["구"].unique(), key="enter_reigon")

    # for col in row2:
    #     tile = col.container(height=100, border=True)
    #     tile.slider("연도 선택", 2011, 2025, (2011, 2025), key="enter_year")

    with row3.container(height=400, border=True):
        chart = alt.Chart(enter_crime[enter_crime["자치구"].isin(select_reigon)]).mark_point().encode(x="업소 갯수", y="범죄수",tooltip=[alt.Tooltip("자치구"), alt.Tooltip("업소 갯수"), alt.Tooltip("범죄수")]).properties(title="자치구별 유흥업소 & 범죄 수 산점도")
        st.altair_chart(chart, use_container_width=True)
    with row4.container(height=400, border=True):
        st.text("유흥업소 갯수별 범죄 발생 비율")
        st.write(f"약 {round(enter_crime["범죄율"].mean())}%로, 유흥업소가 많은 지역일수록 실제로 범죄 발생 건수가 많다.")
        st.write(f"Correlation : {corr[0]}")
        st.write(f"p-value : {corr[1]}")

    with row5:
        enter_map()
    row6.container(height=500, border=True).dataframe(enter[["사업장명", "구", "도로명전체주소"]], height=450)