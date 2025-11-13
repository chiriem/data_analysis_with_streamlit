import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import os
import matplotlib.font_manager as fm # 한글 폰트 관련 용도
from vega_datasets import data
import altair as alt
import scipy.stats as stats

@st.cache_data
def get_cctv():
    cctv = pd.read_excel("./data/seoul_cctv_byyear.xlsx")
    cctv = cctv.set_index("자치구")
    cctv = cctv.rename(columns={"2016년 이전":"2016년", "2025년(6월30일)":"2025년"})
    cctv = cctv.T
    return cctv

@st.cache_data
def get_cctv_wgs84():
    cctv_wgs84 = pd.read_excel("./data/seoul_cctv_loc.xlsx")
    return cctv_wgs84

@st.cache_data
def get_cctv_test():
    cctv_test = pd.read_csv("./data/cctv_테스트.csv")
    return cctv_test

@st.cache_data
def get_crime_test():
    crime_test = pd.read_csv("./data/crime_테스트.csv")
    return crime_test

@st.cache_data
def get_rate():
    rate = pd.read_csv("./data/cctv_개찐막.csv")
    return rate

@st.cache_data
def get_cctv_crime():
    cctv = pd.read_csv("./data/cctv_끝.csv")
    return cctv

@st.cache_data
def my_map():
    cctv_wgs84 = get_cctv_wgs84()
    m = folium.Map(location=[cctv_wgs84["위도"].mean(), cctv_wgs84["경도"].mean()], zoom_start=12, width=800)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in cctv_wgs84.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
        ).add_to(marker_cluster)
    folium.TileLayer('cartodbpositron').add_to(m)
    # st_data = st_folium(m, width=500, height=500)
    folium_static(m)

@st.cache_data
<<<<<<< HEAD
def pearson():
    cctv = get_cctv_crime()
    corr = stats.pearsonr(cctv["CCTV"], cctv["Crime"])
    return corr
=======
def cctv_loc():
        
    df_gu = pd.read_excel("seoul_cctv_loc.xlsx")

    gu_list = ["전체"]

    for i in df_gu["자치구"].unique():
        gu_list.append(i)

    area = st.selectbox("자치구", gu_list)

    if area != "전체":
        df_gu = df_gu[df_gu["자치구"] == area]
        focus_on = [df_gu["위도"].mean(), df_gu["경도"].mean()]

        locations = []
        names = []

        for i in range(len(df_gu)):
            data = df_gu.iloc[i]
            locations.append((float(data["위도"]), float(data["경도"])))
            # names.append(f"{data["CCTV 수량"]}")

        map_gu = folium.Map(location = focus_on, zoom_start = 13)
        
        marker_cluster = MarkerCluster(
            locations= locations,
            # popups = names,
            name = area,
            overlay = True, # 다른 레이어와 겹치기 허용
            control = True, # 레이어 on/off 박스 표시
        )

        marker_cluster.add_to(map_gu)
        folium.LayerControl().add_to(map_gu) # 컨트롤 박스 적용


    else:
        df_gu = pd.read_excel("cctv_count.xlsx")
        focus_on = [df_gu["위도"].mean(), df_gu["경도"].mean()]
        map_gu = folium.Map(location = focus_on, zoom_start = 11, min_zoom = 11, max_zoom = 11, zoom_control= False)

        for i in range(len(df_gu)):
            data = df_gu.iloc[i]
            iframe = folium.IFrame(f"{data["자치구"]} <br> {data["CCTV 수량"]}개")
            popup = folium.Popup(iframe, min_width=100, max_width= 300)
            folium.Marker([data["위도"], data["경도"]], popup=popup).add_to(map_gu)
        
    folium_static(map_gu)
>>>>>>> 7982b09d9f2102232759a8462076f7f134a89e6f

def run_cctv_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([7, 3])
    row5, row6 = st.columns([4, 6])

    cctv = get_cctv()
    corr = pearson()
    cctv_crime = get_cctv_crime()

    for col in row1:
        tile = col.container(height=170, border=True)
        cctv_reigon = tile.multiselect(
            "자치구 선택",
            [i for i in cctv.columns],
            default=[i for i in cctv.columns], key="cctv_reigon")

    for col in row2:
        tile = col.container(height=100, border=True)
        cctv_value = tile.slider("연도 선택", 2016, 2024, (2016, 2024), key="cctv_year")
    
    with row3.container(height=400, border=True):
        chart = alt.Chart(cctv_crime[cctv_crime["자치구"].isin(cctv_reigon)]).mark_point().encode(x="CCTV", y="Crime",tooltip=[alt.Tooltip("자치구"), alt.Tooltip("CCTV"), alt.Tooltip("Crime")]).properties(title="자치구별 CCTV & 범죄 수 산점도")
        st.altair_chart(chart, use_container_width=True)
    
    with row4.container(height=400, border=True):
        st.header("FUCK YOU")
        st.write(f"Correlation : {corr[0]}")
        st.write(f"p-value : {corr[1]}")

    with row5:
        my_map()
    row6.container(height=500, border=True).dataframe(cctv.T, height=450)