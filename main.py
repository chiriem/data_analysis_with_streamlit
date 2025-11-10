import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import matplotlib.font_manager as fm # 한글 폰트 관련 용도

from cctv_app import run_cctv_app

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

def main():
    menu = ['Home', 'CCTV', 'ML', 'About']
    choice = st.sidebar.selectbox("menu", menu)
    if choice == "Home":
        st.subheader("Home")
    elif choice == "CCTV":
        run_cctv_app()
    elif choice == "ML":
        st.subheader("ML")
    elif choice == "About":
        st.subheader("About")
    else: 
        pass

    # # matplotlib 한글 깨짐 방지 장치
    # fontRegistered()
    # plt.rc('font', family="Malgun Gothic")

    # st.title("차트 그리기")

    # scy_df = pd.read_excel("seoul_cctv_byyear.xlsx")

    # st.dataframe(scy_df)

    # df_jongno = scy_df.iloc[0,1:]

    # # 차트 그리기
    # fig = plt.figure()
    # plt.bar(df_jongno.index, df_jongno)
    # plt.title("연도별 종로구 cctv 수")
    # plt.xlabel("년도")
    # plt.ylabel("갯수")
    # st.pyplot(fig)

if __name__ == "__main__":
    main()

