import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # 또는 다른 한글 폰트

# 파일 로드
@st.cache_data
def load_data():
    try:
        df_major_total = pd.read_csv("major_total.csv", encoding="utf-8")
        df_summary = pd.read_csv("정리.csv", encoding="utf-8-sig")
        return df_major_total, df_summary
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
        return None, None
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {str(e)}")
        return None, None

df_major_total, df_summary = load_data()

if df_major_total is None or df_summary is None:
    st.stop()

# UI 설정
st.title("전공별 연관 분석")

# 전공 선택 필터
target_major = st.selectbox("분포를 확인할 전공을 선택하세요:", df_major_total['전공'].unique())

# 전공 등장 여부 확인
def get_related_majors(df, target_major):
    related_majors = []
    for _, row in df.iterrows():
        try:
            majors = [row['첫번째 전공'], row['두번째 전공'], row['세번째 전공']]
            if target_major in majors:
                majors.remove(target_major)  # 선택된 전공 제외
                related_majors.extend([m for m in majors if pd.notna(m) and str(m).strip()])
        except KeyError:
            st.error("데이터프레임의 열 이름을 확인해주세요.")
            return []
    return related_majors

# 연관 전공 데이터 추출
related_majors = get_related_majors(df_summary, target_major)

if related_majors:
    # 데이터 시각화 (원형 차트)
    st.subheader(f"'{target_major}'와 함께 등장한 전공 분포")
    major_counts = pd.Series(related_majors).value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(major_counts, 
                                     labels=major_counts.index, 
                                     autopct='%1.1f%%', 
                                     startangle=90, 
                                     counterclock=False)
    
    # 글자 크기 조정
    plt.setp(autotexts, size=8)
    plt.setp(texts, size=8)
    
    ax.set_aspect('equal')  # 원형 유지
    
    st.pyplot(fig)
else:
    st.write("해당 전공과 함께 등장한 다른 전공이 없습니다.")
