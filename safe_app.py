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
import scipy.stats as stats

@st.cache_data
def get_safe():
    safe = pd.read_csv("./data/safe_wgs84.csv")
    safe = safe[safe['latitude'].notnull()]
    return safe

@st.cache_data
def get_safe_crime():
    safe_crime = pd.read_csv("./data/지킴이집_찐막.csv")
    return safe_crime

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
    folium_static(m)

@st.cache_data
def pearson():
    data = get_safe_crime()
    cor = stats.pearsonr(data["지킴이집 갯수"], data["범죄수"])
    return cor

def run_safe_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([7, 3])
    row5, row6 = st.columns([4, 6])

    safe = get_safe()

    for col in row1:
        tile = col.container(height=170, border=True)
        select_reigon = tile.multiselect(
            "자치구 선택",
            safe["자치구"].unique(),
            default=safe["자치구"].unique(), key="safe_reigon")

    # for col in row2:
    #     tile = col.container(height=100, border=True)
    #     tile.slider("연도 선택", 2011, 2025, (2011, 2025), key="safe_year")
    safe_crime = get_safe_crime()

    with row3.container(height=400, border=True):
        chart = alt.Chart(safe_crime[safe_crime["자치구"].isin(select_reigon)]).mark_point().encode(x="지킴이집 갯수", y="범죄수",tooltip=[alt.Tooltip("자치구"), alt.Tooltip("지킴이집 갯수"), alt.Tooltip("범죄수")]).properties(title="자치구별 지킴이집 & 범죄 수 산점도")
        st.altair_chart(chart, use_container_width=True)
    with row4.container(height=400, border=True):
        cor = pearson()
        st.text("여성안심지킴이집과 범죄 발생의 상관관계")
        st.write(f"Correlation : {cor[0]}")
        st.write(f"p-value : {cor[1]}")
        st.write("여성안심지킴이집이 많이 구비된 강남구는 오히려 범죄발생건수가 가장 높다.")
        st.write("여성안심지킴이집이 많아도 범죄 감소에 영향을 주지 않는다고 판단할 수 있다.")
        st.write("해당 시설이 제 역할을 못하고 있다고 보여진다.")

    with row5:
        my_map()
    row6.container(height=500, border=True).dataframe(safe_crime)
    # row6.container(height=500, border=True).dataframe(safe[["자치구", "브랜드", "소재지"]], height=450)