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

def style_function(feature):
    return {
        'opacity': 0.7,
        'weight': 1,
        'color': 'white',
        'fillOpacity': 0.2,
        'dashArray': '5, 5',
    }

@st.cache_data
def get_reigon():
    reigon = pd.read_csv("./data/구별범죄통계.csv")
    reigon = reigon.set_index("자치구")
    return reigon

def run_reigon_app():
    st.header("자치구별 범죄 발생률")

    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([5, 5])
    row5, row6 = st.columns([4, 6])
    reigon = get_reigon()
    for col in row1:
        tile = col.container(height=170, border=True)
        reigon_select = tile.multiselect(
            "자치구 선택",
            [i for i in reigon.index],
            default=[i for i in reigon.index], key="crime_reigon")

    for col in row2:
        tile = col.container(height=100, border=True)
        value = tile.slider("연도 선택", 2014, 2025, (2014, 2025), key="crime_year")

    with row3.container(height=600, border=True):

        ko = folium.Map(
            location=[37.5651, 126.98955], 
            zoom_start=11,
            tiles='cartodbpositron'
            )
        
        geo_path = './data/seoul_municipalities_geo_simple.json'
        geo_str = json.load(open(geo_path, encoding='utf-8'))

        folium.GeoJson(
            geo_str,
            style_function=style_function
        ).add_to(ko)
        reigon = reigon.loc[reigon_select, f"{value[0]}":f"{value[1]}"].sum(axis=1).to_frame(name="범죄발생수")


        kmap = folium.Choropleth(
            geo_data=geo_str,
            data=reigon,
            columns=[reigon.index, "범죄발생수"],
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            key_on='properties.name',
            legend_name=f"{value[0]}~{value[1]} 범죄 발생수"
        ).add_to(ko)

        # 툴팁처리 추가
        kmap.geojson.zoom_on_click = False
        kmap.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'],labels=False) # Tooltip
        )


        folium_static(ko)

    row4.container(height=600, border=True).dataframe(reigon)