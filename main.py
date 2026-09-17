import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

# 메인 타이틀
st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

# 데이터 불러오기 및 전처리 함수
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # 1. 개봉일(openDt) 날짜 형식을 YYYY-MM-DD 형태로 변환
    df['openDt'] = pd.to_datetime(df['openDt'].astype(str), format='%Y%m%d', errors='coerce')
    
    # 2. 장르(genre) 세로막대 기호(|)로 여러 개 기재된 경우 첫 번째 장르만 추출
    df['primary_genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip() if x != 'nan' else '기타')
    
    return df

# 데이터 로드
df = load_data()

# -------------------------------------------------------------------
# 1. 장르별 영화 편수 (플롯리 도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

# 장르별 편수 집계
genre_counts = df['primary_genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 편수']

# Plotly 도넛 차트 생성
fig = px.pie(
    genre_counts,
    names='장르',
    values='영화 편수',
    hole=0.4,
    title="주요 장르별 영화 비율"
)

# 마우스오버 시 편수와 비율이 함께 표시되도록 설정
fig.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 구분선 및 인사이트 섹션
st.divider()
st.info("**이 그래프로 알 수 있는 것:** 박스오피스 상위권 영화 중 특정 주요 장르가 차지하는 비중과 분포 상태를 한눈에 비교할 수 있습니다.")
