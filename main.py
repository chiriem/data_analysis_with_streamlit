import streamlit as st
import altair as alt
import os
import matplotlib.font_manager as fm # 한글 폰트 관련 용도
from cctv_app import run_cctv_app
from bell_app import run_bell_app
from safe_app import run_safe_app
from enter_app import run_enter_app
from reigon_app import run_reigon_app
from time_app import run_time_app
from populaion_app import run_population_app
from office_app import run_office_app

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

def main():
    page_config()
    st.title("서울특별시 범죄발생률 감소요인 분석")

    tab_region, tab_time, tab_bell, tab_cctv, tab_enter, tab_popul, tab_safe, tab_police = st.tabs(["지역별 범죄 발생률", "시간대별 범죄 발생률", "비상안전벨", "CCTV", "유흥업소", "인구밀집도", "여성안심지킴이집", "파출소"])
    with tab_region:
        run_reigon_app()

    with tab_bell:
        run_bell_app()

    with tab_cctv:
        run_cctv_app()

    with tab_time:
        run_time_app()

    with tab_enter:
        run_enter_app()

    with tab_popul:
        run_population_app()

    with tab_safe:
        run_safe_app()

    with tab_police:
        run_office_app()

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

if __name__ == "__main__":
    main()

