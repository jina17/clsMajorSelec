import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 한글 자동 적용

def load_data():
    # 데이터 로드
    indivi_major = pd.read_csv("indivi_major.csv")
    major_total = pd.read_csv("major_total.csv")
    return indivi_major, major_total

def plot_major_distribution(df, selected_major):
    # 선택한 전공이 등장한 위치에 따라 나머지 전공들의 분포 확인
    first_major_mask = df['첫번째 전공'] == selected_major
    second_major_mask = df['두번째 전공'] == selected_major
    third_major_mask = df['세번째 전공'] == selected_major
    
    combined_distribution = pd.Series(dtype=int)
    
    if first_major_mask.sum() > 0:
        combined_distribution = combined_distribution.add(df.loc[first_major_mask, '두번째 전공'].value_counts(), fill_value=0)
    if second_major_mask.sum() > 0:
        combined_distribution = combined_distribution.add(df.loc[second_major_mask, '첫번째 전공'].value_counts(), fill_value=0)
    if third_major_mask.sum() > 0:
        combined_distribution = combined_distribution.add(df.loc[third_major_mask, '첫번째 전공'].value_counts(), fill_value=0)
    
    return combined_distribution.sort_values(ascending=False)

def main():
    st.title("전공 분포 분석")
    
    # 데이터 로드
    indivi_major, major_total = load_data()
    
    # 전공 선택
    major_list = major_total['전공'].unique()
    selected_major = st.selectbox("전공 선택", major_list)
    
    # 데이터 필터링 및 그래프 생성
    distribution = plot_major_distribution(indivi_major, selected_major)
    
    if not distribution.empty:
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(
            distribution,
            labels=[label if value / distribution.sum() >= 0.03 else "" for label, value in zip(distribution.index, distribution)],
            autopct=lambda p: f'{p:.1f}%' if p >= 3 else '',
            startangle=90
        )
        ax.axis('equal')
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.write("선택한 전공과 함께 등장하는 다른 전공이 없습니다.")

if __name__ == "__main__":
    main()
