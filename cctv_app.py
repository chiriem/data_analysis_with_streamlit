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

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

def run_cctv_app():

    # matplotlib 한글 깨짐 방지 장치
    fontRegistered()
    plt.rc('font', family="Malgun Gothic")

    # 메뉴 지정
    submenu = st.sidebar.selectbox("submenu", ['연도별 CCTV', 'CCTV 위치', '분석'])
    if submenu == "submenu":
        st.subheader("submenu")
    elif submenu == "연도별 CCTV":
        st.title("차트 그리기")
        
        scy_df = pd.read_excel("seoul_cctv_byyear.xlsx", index_col="자치구")
        
        st.dataframe(scy_df)

        a, b = st.slider("년도 선택", 2016, 2025, (2022, 2023))

        a = str(a) + "년"
        b = str(b) + "년"

        x = []

        for i in range(2016, 2026):
            x.append(str(i)+"년")

        scy_df.columns = x

        area = st.selectbox("자치구", scy_df.T.columns)

        scy_df = scy_df[[a, b]].loc[[area], :].T
        scy_df_s = scy_df[area]
        titletext = "연도별 " + area + " cctv 수"

        # 차트 그리기
        fig = plt.figure()

        plt.bar(scy_df_s.index, scy_df_s)
        plt.title(titletext)
        plt.xlabel("년도")
        plt.ylabel("갯수")
        st.pyplot(fig)
        
        inc = (scy_df.T[b] - scy_df.T[a]) / scy_df.T[b] * 100
        st.markdown(f"## {a} 대비 {b} 증감률")
        st.markdown(f"### {inc[0].round(1)}% 증가")

    elif submenu == "CCTV 위치":
        st.subheader("CCTV 위치")

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
            map_gu = folium.Map(location = focus_on, zoom_start = 11, zoom_control= False)

            for i in range(len(df_gu)):
                data = df_gu.iloc[i]
                iframe = folium.IFrame(f"{data["자치구"]} <br> {data["CCTV 수량"]}개")
                popup = folium.Popup(iframe, min_width=100, max_width= 300)
                folium.Marker([data["위도"], data["경도"]], popup=popup).add_to(map_gu)
        


        folium_static(map_gu)
        


    elif submenu == "분석":
        st.subheader("분석")
    else: 
        pass
    