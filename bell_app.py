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
import scipy.stats as stats

@st.cache_data
def get_data():
    bell_df = pd.read_csv("./data/비상벨.csv", index_col=0)
    return bell_df

@st.cache_data
def get_bell_wgs84():
    bell = pd.read_csv("./data/비상벨그만.csv")
    return bell

@st.cache_data
def get_bell_crime():
    bell_crime = pd.read_csv("./data/장석원의마지막불꽃.csv")
    return bell_crime

@st.cache_data
def get_pearson():
    data = get_bell_crime()
    cor = stats.pearsonr(data["누적안전벨 수"], data["범죄수"])
    return cor

@st.cache_data
def my_map():
    bell_df = get_bell_wgs84()

    bell_df[["lat","lon"]] = bell_df[["WGS84위도","WGS84경도"]]
    m = folium.Map(location=[bell_df["lat"].mean(), bell_df["lon"].mean()], zoom_start=12, width=800)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in bell_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=[row.name, row["lat"], row["lon"]],
        ).add_to(marker_cluster)
    folium.TileLayer('cartodbpositron').add_to(m)
    
    folium_static(m)

def run_bell_app():
    #row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([7, 3])
    row5, row6 = st.columns([4, 6])

    bell_df = get_data()

    # for col in row1:
    #     tile = col.container(height=170, border=True)
    #     select_reigon = tile.multiselect(
    #         "자치구 선택",
    #         bell_df["구"].unique(),
    #         default=bell_df["구"].unique(), key="bell_reigon")

    for col in row2:
        tile = col.container(height=100, border=True)
        b_value = tile.slider("연도 선택", 2014, 2024, (2014, 2024), key="bell_year")

    with row3.container(height=400, border=True):
        bell_crime = get_bell_crime()
        bell_crime = bell_crime.set_index("연도")
        st.line_chart(data = bell_crime.loc[f"{b_value[0]}" : f"{b_value[1]}", ["누적안전벨 수", "범죄수"]], x_label="연도", y_label="안전비상벨 수 & 범죄 수", color=["#1656AD","#D30000"])
        # chart = alt.Chart().mark_line().encode().properties()
        # st.altair_chart(chart, use_container_width=True)

    with row4.container(height=400, border=True):
        cor = get_pearson()
        st.text("비상안전벨과 범죄 발생의 상관관계")
        st.write(f"Correlation : {cor[0]}")
        st.write(f"p-value : {cor[1]}")
        st.write("2022년도에는 비상안전벨이 더 많아졌지만, 범죄 발생 건수도 올라갔다.")
        st.write("p-value가 0.05보다 훨씬 낮고, 높은 음의 상관관계를 갖고 있기 때문에 우연적으로 올라갔다고 판단할 수 있다.")
        st.write("결론적으로 비상안전벨의 증가는 범죄 감소에 영향이 있다고 볼 수 있다.")

    with row5:
        my_map()
    row6.container(height=500, border=True).dataframe(bell_df[["설치연도", "구"]], height=450)