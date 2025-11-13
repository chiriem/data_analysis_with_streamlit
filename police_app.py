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
def get_police():
    police = pd.read_csv("./data/파출소_자치구.csv")
    return police

@st.cache_data
def get_office():
    office = pd.read_excel("./data/police_crime.xlsx")
    return office

@st.cache_data
def get_police_crime():
    police_crime = pd.read_csv("./data/파출소_범죄.csv")
    return police_crime

@st.cache_data
def police_map():
    police = get_police()
    m = folium.Map(location=[police["Latitude"].mean(), police["Longitude"].mean()], zoom_start=12, width=800)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in police.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
        ).add_to(marker_cluster)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium_static(m)

@st.cache_data
def pearson():
    data = get_office()
    cor = stats.pearsonr(data["인구수/파출소수"], data["범죄수"])
    return cor

def run_police_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([7, 3])
    row5, row6 = st.columns([4, 6])

    police = get_police()
    office = get_office()
    police_crime = get_police_crime()

    for col in row1:
        tile = col.container(height=170, border=True)
        select_reigon = tile.multiselect(
            "자치구 선택",
            police["구"].unique(),
            default=police["구"].unique(), key="police_reigon")

    # for col in row2:
    #     tile = col.container(height=100, border=True)
    #     tile.slider("연도 선택", 2011, 2025, (2011, 2025), key="enter_year")

    with row3.container(height=400, border=True):
        # chart = alt.Chart(police_crime[police_crime["자치구"].isin(select_reigon)]).mark_point().encode(x="파출소 수", y="범죄수",tooltip=[alt.Tooltip("자치구"), alt.Tooltip("파출소 수"), alt.Tooltip("범죄수")]).properties(title="자치구별 파출소 & 범죄 수 산점도")
        # st.altair_chart(chart, use_container_width=True)
        chart = alt.Chart(office[office["자치구"].isin(select_reigon)]).mark_point().encode(x="인구수/파출소수", y="범죄수", tooltip=[alt.Tooltip("자치구"), alt.Tooltip("인구수/파출소수"), alt.Tooltip("범죄수")]).properties(title="자치구별 파출소 당 관리 인구 수 & 범죄 수 산점도")
        st.altair_chart(chart, use_container_width=True)
    with row4.container(height=400, border=True):
        st.text("파출소 당 관리인구수와 범죄 발생 비율")
        # st.write(f"약 {round((office["범죄수"]/office["인구수/파출소수"]).mean())}%")
        cor = pearson()
        st.write(f"Correlation : {cor[0]}")
        st.write(f"p-value : {cor[1]}")
        st.write("파출소 수가 많다고해서 범죄 발생 감소의 기대치를 보긴 힘들다고 볼 수 있다.")

    with row5:
        police_map()
    row6.container(height=500, border=True).dataframe(office)
    # row6.container(height=500, border=True).dataframe(police[["이름", "구", "도로명주소"]], height=450)