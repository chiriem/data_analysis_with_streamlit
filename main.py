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

if __name__ == "__main__":
    main()

