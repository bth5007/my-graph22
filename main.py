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
    
    # 2. 장르(genre) 처리: str.split('|')을 사용하여 첫 번째 장르만 추출 후 결측치는 '기타'로 채움
    df['primary_genre'] = df['genre'].astype(str).str.split('|').str[0].str.strip()
    df['primary_genre'] = df['primary_genre'].replace(['nan', 'None', ''], '기타').fillna('기타')
    
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
fig1 = px.pie(
    genre_counts,
    names='장르',
    values='영화 편수',
    hole=0.4,
    title="주요 장르별 영화 비율"
)

# 마우스오버 시 편수와 비율이 함께 표시되도록 설정
fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# 구분선 및 인사이트 섹션
st.info("**이 그래프로 알 수 있는 것:** 박스오피스 상위권 영화 중 특정 주요 장르가 차지하는 비중과 분포 상태를 한눈에 비교할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 2. 장르 및 영화별 총 관객수 (플롯리 트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포")

# Plotly 트리맵 차트 생성
fig2 = px.treemap(
    df,
    path=['primary_genre', 'movieNm'],  # 계층 구조: 장르 -> 영화명
    values='total_audi',                # 사각형 크기: 총 관객수
    color='primary_genre',              # 장르별 색상 구분
    title="장르 및 영화별 총 관객수 트리맵"
)

# 마우스오버 시 영화명(label)과 총 관객수(value)가 보이도록 설정
fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,.0f}명<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 구분선 및 인사이트 섹션
st.info("**이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 흥행을 주도했는지, 장르 전체 관객수 대비 개별 영화의 관객수 비중을 한눈에 파악할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 3. 총 관객수 분포 (플롯리 히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객수(total_audi) 분포")

# Plotly 히스토그램 생성
fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객수 히스토그램",
    labels={'total_audi': '총 관객수(명)', 'count': '영화 수'}
)

fig3.update_traces(
    hovertemplate="<b>관객수 구간: %{x:,.0f}명</b><br>해당 구간 영화 수: %{y}편<extra></extra>"
)

# Streamlit에 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 가장 관객이 많은 영화 정보 추출
top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

# 인사이트 및 분석 문구 출력
st.info(
    f"**이 그래프로 알 수 있는 것:** большинство의 영화는 **100만~300만 명 이하의 구간**에 대다수 밀집해 있는 롱테일 분포 양상을 보입니다. "
    f"또한, 본 데이터셋에서 가장 관객이 많은 영화는 **'{top_movie_name}'**(약 {top_movie_audi:,.0f}명)입니다."
)
