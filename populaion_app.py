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

def to_pivot(value):
    return value.pivot_table(index = "시군구명", columns= "연도", values= "총인구수", aggfunc= "mean").astype(int)

@st.cache_data
def get_region():
    region = pd.read_excel("./data/real_서울인구.xlsx")
    region = region.set_index("구")
    region = region.iloc[1:,:]
    return region

def run_population_app():
    st.header("자치구별 인구 수")

    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([5, 5])
    row5, row6 = st.columns([4, 6])
    region = get_region()
    for col in row1:
        tile = col.container(height=170, border=True)
        region_select = tile.multiselect(
            "자치구 선택",
            [i for i in region.index],
            default=[i for i in region.index], key="population_region")

    for col in row2:
        tile = col.container(height=100, border=True)
        value = tile.slider("연도 선택", 2017, 2024, key="population_year")

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
        region = region.loc[region_select, f"{value}년"].to_frame(name="인구 수")


        kmap = folium.Choropleth(
            geo_data=geo_str,
            data=region,
            columns=[region.index, "인구 수"],
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            key_on='properties.name',
            legend_name=f"{value} 인구 수"
        ).add_to(ko)

        # 툴팁처리 추가
        kmap.geojson.zoom_on_click = False
        kmap.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'],labels=False) # Tooltip
        )


        folium_static(ko)

    row4.container(height=600, border=True).dataframe(region)