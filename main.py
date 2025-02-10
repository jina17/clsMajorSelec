import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 파일 로드
@st.cache_data
def load_data():
    df_major_total = pd.read_csv("major_total.csv", encoding="utf-8")
    df_summary = pd.read_csv("정리.csv", encoding="utf-8-sig")
    return df_major_total, df_summary

df_major_total, df_summary = load_data()

# UI 설정
st.title("전공별 연관 분석")

# 전공 선택 필터
target_major = st.selectbox("분포를 확인할 전공을 선택하세요:", df_major_total['전공'].unique())

# 전공 등장 여부 확인
def get_related_majors(df, target_major):
    related_majors = []
    for _, row in df.iterrows():
        if target_major in [row['첫번째 전공'], row['두번째 전공'], row['세번째 전공']]:
            majors = [row['첫번째 전공'], row['두번째 전공'], row['세번째 전공']]
            majors.remove(target_major)  # 선택된 전공 제외
            related_majors.extend([m for m in majors if pd.notna(m)])
    return related_majors

# 연관 전공 데이터 추출
related_majors = get_related_majors(df_summary, target_major)

if related_majors:
    # 데이터 시각화 (원형 차트)
    st.subheader(f"'{target_major}'와 함께 등장한 전공 분포")
    major_counts = pd.Series(related_majors).value_counts()
    
    fig, ax = plt.subplots()
    ax.pie(major_counts, labels=major_counts.index, autopct='%1.1f%%', startangle=90, counterclock=False)
    ax.set_aspect('equal')  # 원형 유지
    
    st.pyplot(fig)
else:
    st.write("해당 전공과 함께 등장한 다른 전공이 없습니다.")
