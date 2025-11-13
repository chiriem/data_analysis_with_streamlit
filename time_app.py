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

@st.cache_data
def get_crime():
    crime = pd.read_excel("./data/seoul_crime.xlsx", index_col=0)
    return crime

def run_time_app():
    df = get_crime()
    crime_time = df.iloc[:, 1:9].sum(axis=0)
    c_df = crime_time.to_frame(name="범죄 발생 횟수")
    c_df.reset_index(inplace=True)
    c_df = c_df.rename(columns={"index":"Time"})

    row1, row2 = st.columns([7, 3])
    row3, row4 = st.columns([5, 5])

    with row1.container(height=400, border=True):
        chart = alt.Chart(c_df).mark_bar(color="red").encode(
            x="Time", y="범죄 발생 횟수",
        ).properties(title=alt.Title(text="시간대별 범죄 발생 횟수", align="center", anchor="middle"))
        st.altair_chart(chart)

    with row2.container(height=400, border=True):
        st.write("평균적으로 알코올 섭취와 관련된 시간대에 범죄 발생 비율이 높게 나타나고 있다.")
        st.write("대검찰청, 보건복지부 등의 공공기관 통계자료를 분석한 학술자료에 따르면 알코올은 폭행, 강간, 방화 등 폭력 및 파괴성이 높은 강력 범죄와 높은 상관관계를 보인다고 한다.")
        st.write("따라서 음주와 범죄 사이의 인과관계를 분석하기 위해 서울시 자치구별 유흥업소(단란주점)과 강력범죄와의 분석을 시도한다.")

    with row3.container(height=400, border=True):
        st.text("알코올은 타인에게 어떤 영향을 미치는가?")
        st.image("./image/alc.png")

    with row4.container(height=400, border=True):
        st.header("통계청의 분석 내용")
        st.write("⋄ 중독성 약물 중 술은 가장 피해가 큰 약물이며, 특히 타인에게 미치는 피해가 압도적으로 가장 높다.")
        st.write("⋄ 통계청에 따르면 술과 관련한 사망자 수는 1일 평균 13명이다.")
        st.write("⋄ 연간 약 2만건 가량의 음주운전 사고가 발생한다.")
        st.write("⋄ 강력범죄의 약 30%는 음주 상태에서 발생한다.")

