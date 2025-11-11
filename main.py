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

st.markdown("""
    <style>
    .stVerticalBlock {
        justify-content: center;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

def page_config():
    st.set_page_config(
        page_title="Seoul Crime Analysis",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="auto")
    alt.themes.enable("dark")

option = st.sidebar.selectbox(
    "Menu",
    ("A1", "B1", "C1")
)

@st.cache_data
def get_data():
    sido = json.load(open("./data/SIDO_MAP_2022.json", encoding="utf-8"))
    bell = gpd.read_file("./data/bell.geojson")
    bell_df = pd.read_csv("./data/비상벨.csv", index_col=0)
    return bell_df

@st.cache_data
def get_crime():
    crime = pd.read_excel("./data/seoul_crime.xlsx", index_col=0)
    return crime

@st.cache_data
def get_reigon():
    reigon = pd.read_csv("./data/구별범죄통계.csv")
    reigon = reigon.set_index("자치구")
    return reigon

def loading_bar():
    progress_bar = st.progress(0)

    for percent in range(0, 100, 3):
        time.sleep(0.4)
        progress_bar.progress(percent)
    
    progress_bar.empty()

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
    # st_data = st_folium(m, width=500, height=500)
    folium_static(m)

def style_function(feature):
    return {
        'opacity': 0.7,
        'weight': 1,
        'color': 'white',
        'fillOpacity': 0.2,
        'dashArray': '5, 5',
    }

def main():
    page_config()
    st.title("서울특별시 범죄발생률 감소요인 분석")

    tab_region, tab_time, tab_bell, tab_cctv, tab_enter, tab_popul, tab_safe = st.tabs(["지역별 범죄 발생률", "시간대별 범죄 발생률", "비상안전벨", "CCTV", "유흥업소", "인구밀집도", "여성안심지킴이집"])
    with tab_region:
        st.header("자치구별 범죄 발생률")

        row1 = st.columns(1)
        row2 = st.columns(1)
        row3, row4 = st.columns([5, 5])
        row5, row6 = st.columns([4, 6])

        for col in row1:
            tile = col.container(height=100, border=True)
            tile.multiselect(
                "자치구 선택",
                ["전체", "강남구", "마포구", "서초구", "서대문구"],
                default=["전체"], key="crime_reigon")

        for col in row2:
            tile = col.container(height=100, border=True)
            value = tile.slider("연도 선택", 2011, 2025, (2011, 2025), key="crime_year")

        with row3.container(height=600, border=True):
            reigon = get_reigon()

            ko = folium.Map(
                location=[37.5651, 126.98955], 
                zoom_start=11,
                tiles='cartodb dark_matter'
                )
            
            geo_path = './data/seoul_municipalities_geo_simple.json'
            geo_str = json.load(open(geo_path, encoding='utf-8'))

            folium.GeoJson(
                geo_str,
                style_function=style_function
            ).add_to(ko)
            reigon = reigon.loc[:, f"{value[0]}":f"{value[1]}"].sum(axis=1).to_frame(name="범죄발생수")


            folium.Choropleth(
                geo_data=geo_str,
                data=reigon,
                columns=[reigon.index, "범죄발생수"],
                fill_color='Reds',
                fill_opacity=0.7,
                line_opacity=0.5,
                key_on='properties.name',
                legend_name=f"{value[0]}~{value[1]} 범죄 발생수"
            ).add_to(ko)

            folium_static(ko)

        row4.container(height=600, border=True).title("TEST")

    with tab_bell:
        row1 = st.columns(1)
        row2 = st.columns(1)
        row3, row4 = st.columns([7, 3])
        row5, row6 = st.columns([4, 6])

        bell_df = get_data()

        for col in row1:
            tile = col.container(height=100, border=True)
            tile.multiselect(
                "자치구 선택",
                ["강남구", "마포구", "서초구", "서대문구"],
                default=["서대문구"], key="bell_reigon")

        for col in row2:
            tile = col.container(height=100, border=True)
            tile.slider("연도 선택", 2011, 2025, (2011, 2025), key="bell_year")

        source = data.barley()

        row3.container(height=400, border=True).bar_chart(source, x="variety", y="yield", color="site", horizontal=True)
        row4.container(height=400, border=True).title("Analysis Result")

        with row5:
            my_map()
        row6.container(height=500, border=True).dataframe(bell_df[["설치연도","WGS84위도", "WGS84경도", "구"]], height=450)

    with tab_time:
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

    with tab_enter:
        st.header("Header Test")

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

if __name__ == "__main__":
    main()

