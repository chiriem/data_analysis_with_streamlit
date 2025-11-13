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

def style_function(feature):
    return {
        'opacity': 0.7,
        'weight': 1,
        'color': 'white',
        'fillOpacity': 0.2,
        'dashArray': '5, 5',
    }

@st.cache_data
def get_popul():
    popul = pd.read_csv("./data/서울인구_찐막.csv")
    popul = popul.set_index("구")
    return popul

@st.cache_data
def get_popul_crime():
    # popul_crime = pd.read_csv("./data/인구밀집별_범죄비율.csv")
    popul_crime = pd.read_excel("./data/crime_per_person.xlsx")
    popul_crime = popul_crime.set_index("자치구")
    return popul_crime

@st.cache_data
def get_cnp():
    cnp = pd.read_excel("./data/crime_and_population.xlsx")
    cnp = cnp.set_index("자치구")
    return cnp

def run_popul_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([5, 5])
    row5 = st.columns(1)
    row6, row7 = st.columns([5, 5])
    
    popul = get_popul()

    for col in row1:
        tile = col.container(height=170, border=True)
        reigon_select = tile.multiselect(
            "자치구 선택",
            popul.index,
            default=popul.index, key="popul_reigon")

    for col in row2:
        tile = col.container(height=100, border=True)
        value = tile.slider("연도 선택", 2017, 2024, (2017, 2024), key="popul_year")

    with row3.container(height=650, border=True):
        st.header(f"{value[0]} ~ {value[1]}년 인구밀집도")

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
        reigon = popul.loc[reigon_select, f"{value[0]}년":f"{value[1]}년"].sum(axis=1).to_frame(name="인구수")


        kmap = folium.Choropleth(
            geo_data=geo_str,
            data=reigon,
            columns=[reigon.index, "인구수"],
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            key_on='properties.name',
            legend_name=f"{value[0]}~{value[1]} 인구수"
        ).add_to(ko)

        # 툴팁처리 추가
        kmap.geojson.zoom_on_click = False
        kmap.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'],labels=False) # Tooltip
        )


        folium_static(ko)

    with row4.container(height=650, border=True):
        st.header(f"{value[0]} ~ {value[1]}년 인구밀집별 범죄발생률")
        popul_crime = get_popul_crime()

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
        reigon = popul_crime.loc[reigon_select, f"{value[0]}년":f"{value[1]}년"].mean(axis=1).to_frame(name="범죄/인구 비율")


        kmap = folium.Choropleth(
            geo_data=geo_str,
            data=reigon,
            columns=[reigon.index, "범죄/인구 비율"],
            fill_color='Reds',
            fill_opacity=0.7,
            line_opacity=0.2,
            key_on='properties.name',
            legend_name=f"{value[0]}~{value[1]} 범죄/인구 비율"
        ).add_to(ko)

        # 툴팁처리 추가
        kmap.geojson.zoom_on_click = False
        kmap.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'],labels=False) # Tooltip
        )

        folium_static(ko)

    cnp = get_cnp()

    for col in row5:
        tile = col.container(height=100, border=True)
        value = tile.slider("연도 선택", 2017, 2024, 2024, key="popul_year2")
    
    new_cnp = cnp.loc[:,[f"{value}_인구", f"{value}_범죄"]]
    with row6.container(height=500, border=False):
        st.dataframe(new_cnp)

    with row7.container(height=500, border=True):
        cnp = cnp.reset_index()
        chart = alt.Chart(cnp).mark_point().encode(x = f"{value}_인구",y = f"{value}_범죄",tooltip=[alt.Tooltip("자치구"), alt.Tooltip(f"{value}_인구"), alt.Tooltip(f"{value}_범죄")]).properties(title="자치구별 인구 & 범죄 수 산점도")
        st.altair_chart(chart, use_container_width=True)

    