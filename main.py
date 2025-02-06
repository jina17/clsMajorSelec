import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 백엔드 설정
import matplotlib.pyplot as plt

pip install -r requirements.txt

# 데이터 로드 함수
def load_data():
    student_data_path = "Final_Organized_Graduated_Students.csv"
    major_total_path = "major_total.csv"
    
    df_students = pd.read_csv(student_data_path)
    df_majors = pd.read_csv(major_total_path)
    return df_students, df_majors

df_students, df_majors = load_data()

# 헤더
st.title("Major Analysis by Student ID")
st.markdown("""
이 대시보드는 학생들의 전공 선택과 특정 전공 포함 여부를 분석합니다.
""")

# 전공 포함 여부 확인 함수
def filter_students_by_major(df_students, df_majors):
    major_list = df_majors['전공'].tolist()
    
    def has_major(row):
        return any(row[col] in major_list for col in ['전공1', '전공2', '전공3', '전공4'] if pd.notna(row[col]))
    
    return df_students[df_students.apply(has_major, axis=1)]

df_filtered = filter_students_by_major(df_students, df_majors)

# 필터링된 데이터 표시
st.subheader("Students with Specified Majors")
st.dataframe(df_filtered)

# 원형 차트 생성 함수
def plot_pie_chart(df_filtered, df_majors):
    major_list = df_majors['전공'].tolist()
    
    major_counts = {}
    for _, row in df_filtered.iterrows():
        for col in ['전공1', '전공2', '전공3', '전공4']:
            if pd.notna(row[col]) and row[col] in major_list:
                major_counts[row[col]] = major_counts.get(row[col], 0) + 1
    
    if major_counts:
        fig, ax = plt.subplots()
        ax.pie(major_counts.values(), labels=major_counts.keys(), autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.subheader("Major Distribution Pie Chart")
        st.pyplot(fig)

# 원형 차트 출력
plot_pie_chart(df_filtered, df_majors)
