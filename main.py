import streamlit as st

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="Graduated Students Analysis", layout="wide")

# 데이터 로드
def load_data():
    file_path = "Final_Organized_Graduated_Students.csv"
    return pd.read_csv(file_path)

df = load_data()

# 헤더
st.title("Graduated Students Data Analysis")
st.markdown("""
이 대시보드는 서울대 자유전공학부 졸업생들의 전공 선택 현황을 분석합니다.
각 학생별로 최대 4개의 전공을 선택할 수 있습니다.
""")

# 데이터 표시
st.subheader("Raw Data Preview")
st.dataframe(df)

# 전공별 학생 수 분석
def count_major_occurrences(df):
    majors = df[['전공1', '전공2', '전공3', '전공4']].values.flatten()
    majors = [major for major in majors if pd.notna(major)]
    return pd.Series(majors).value_counts()

st.subheader("Major Selection Distribution")
major_counts = count_major_occurrences(df)

fig, ax = plt.subplots()
major_counts.plot(kind='bar', ax=ax)
ax.set_ylabel("Number of Students")
ax.set_title("Distribution of Selected Majors")
st.pyplot(fig)

# 전공별 필터링
st.subheader("Filter by Major")
selected_major = st.selectbox("Select a major to filter students:", ["All"] + list(major_counts.index))
if selected_major != "All":
    df_filtered = df[df.isin([selected_major]).any(axis=1)]
else:
    df_filtered = df
st.dataframe(df_filtered)

# 학번 검색 기능
st.subheader("Search by Student ID")
search_id = st.text_input("Enter student ID:")
if search_id:
    search_results = df[df['학번'].astype(str).str.contains(search_id, na=False)]
    st.dataframe(search_results)

# 앱 종료
st.markdown("---")
st.write("Developed for analyzing graduated students' major selection trends.")
