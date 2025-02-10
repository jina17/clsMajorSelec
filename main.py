import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.title("서울대 자유전공학부 전공선택현황")
    
    # 데이터 로드
    indivi_major, major_total = load_data()
    
    # 전공 선택
    major_list = major_total['전공'].unique()
    selected_major = st.selectbox("확인하고 싶은 전공을 선택해주세요", major_list)
    
    # 데이터 필터링 및 그래프 생성
    distribution = plot_major_distribution(indivi_major, selected_major)
    
    if not distribution.empty:
        df_plot = pd.DataFrame({"전공": distribution.index, "수량": distribution.values})
        
        # Plotly 원형 차트 사용하여 호버 기능 추가
        fig = px.pie(df_plot, names='전공', values='수량', title=f'"{selected_major}"을 선택한 학생들이 선택한 전공들',
                     hover_data=['수량'], labels={'수량': '비율'}, hole=0.3)
        fig.update_traces(textinfo='percent+label', textposition='inside', hoverinfo='label+value+percent')
        
        # 범례 제거 및 차트 크기 확대
        fig.update_layout(showlegend=False, height=700, width=700)
        
        st.plotly_chart(fig)
    else:
        st.write("선택한 전공과 함께 등장하는 다른 전공이 없습니다.")

if __name__ == "__main__":
    main()
