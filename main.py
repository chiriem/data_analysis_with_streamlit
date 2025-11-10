import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# windows용 한글 폰트 오류 해결
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname= font_path).get_name()
rc("font", family = font_name)

def main():

    st.markdown("# Hello Strealit")
    st.write(np.__version__)

if __name__ == "__main__":
    main()

st.title("차트 그리기")

scy_df = pd.read_excel("seoul_cctv_byyear.xlsx")

st.dataframe(scy_df)

df_jongno = scy_df.iloc[0,1:]

# 차트 그리기
fig = plt.figure()
plt.bar(df_jongno.index, df_jongno)
plt.title("연도별 종로구 cctv 수")
plt.xlabel("년도")
plt.ylabel("갯수")
st.pyplot(fig)