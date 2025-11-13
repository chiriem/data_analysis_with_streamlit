import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import os
import matplotlib.font_manager as fm # 한글 폰트 관련 용도
import geopandas as gpd
import time
from vega_datasets import data

@st.cache_data
def get_office():
    office = pd.read_excel("./data/police_crime.xlsx")
    return office

def run_office_app():
    row1 = st.columns(1)
    row2 = st.columns(1)
    row3, row4 = st.columns([6, 4])
    row5, row6 = st.columns([4, 6])

    office = get_office()

    # source = data.barley()

    with row3.container(height=400, border=True):
        chart = alt.Chart(office).mark_point().encode(x="인구수/파출소수", y="범죄수", tooltip=[alt.Tooltip("자치구"), alt.Tooltip("인구수/파출소수"), alt.Tooltip("범죄수")]).properties(title="자치구별 파출소 당 관리 인구 수 & 범죄 수 산점도")
        st.altair_chart(chart, use_container_width=True)
    row4.container(height=400, border=True).text("파출소 당 관리하는 인구 수와 범죄 수가 비례하여 커지는 경향이 있음\n따라서 둘은 양의 상관관계라 할 수 있음")
    # row6.container(height=500, border=True).dataframe(office[["사업장명", "구", "도로명전체주소"]], height=450)