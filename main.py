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
    
    # 3. 제작 국가(nation) 결측치 및 빈 문자열 처리
    df['nation'] = df['nation'].fillna('기타국가').astype(str).str.strip()
    df['nation'] = df['nation'].replace('', '기타국가')
    
    return df

# 데이터 로드
df = load_data()

# -------------------------------------------------------------------
# 1. 장르별 영화 편수 (플롯리 도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 분포")

genre_counts = df['primary_genre'].value_counts().reset_index()
genre_counts.columns = ['장르', '영화 편수']

fig1 = px.pie(
    genre_counts,
    names='장르',
    values='영화 편수',
    hole=0.4,
    title="주요 장르별 영화 비율"
)

fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

st.plotly_chart(fig1, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** 박스오피스 상위권 영화 중 특정 주요 장르가 차지하는 비중과 분포 상태를 한눈에 비교할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 2. 장르 및 영화별 총 관객수 (플롯리 트리맵)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객수 분포")

fig2 = px.treemap(
    df,
    path=['primary_genre', 'movieNm'],
    values='total_audi',
    color='primary_genre',
    title="장르 및 영화별 총 관객수 트리맵"
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>총 관객수: %{value:,.0f}명<extra></extra>"
)

st.plotly_chart(fig2, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** 각 장르 내에서 어떤 영화가 흥행을 주도했는지, 장르 전체 관객수 대비 개별 영화의 관객수 비중을 한눈에 파악할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 3. 총 관객수 분포 (플롯리 히스토그램)
# -------------------------------------------------------------------
st.subheader("3. 총 관객수(total_audi) 분포")

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

st.plotly_chart(fig3, use_container_width=True)

top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

st.info(
    f"**이 그래프로 알 수 있는 것:** 대부분의 영화는 **100만~300만 명 이하의 구간**에 대다수 밀집해 있는 롱테일 분포 양상을 보입니다. "
    f"또한, 본 데이터셋에서 가장 관객이 많은 영화는 **'{top_movie_name}'**(약 {top_movie_audi:,.0f}명)입니다."
)

st.divider()

# -------------------------------------------------------------------
# 4. 개봉일 스크린수 vs 총 관객수 (산점도)
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객수의 관계")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='primary_genre',
    hover_name='movieNm',
    title="개봉일 스크린수 vs 총 관객수 산점도",
    labels={'first_scrn': '개봉일 스크린수', 'total_audi': '총 관객수(명)', 'primary_genre': '장르'}
)

fig4.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x}개<br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** 개봉 초기 확보한 스크린수가 최종 총 관객수 확보에 어느 정도 긍정적인 영향을 미치는지 직관적인 상관관계를 확인할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 5. 장르별 총 관객수 분포 (상자 그림 / 박스플롯)
# -------------------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객수 분포 (10편 이상 장르)")

genre_counts_series = df['primary_genre'].value_counts()
target_genres = genre_counts_series[genre_counts_series >= 10].index
df_filtered_box = df[df['primary_genre'].isin(target_genres)]

fig5 = px.box(
    df_filtered_box,
    x='primary_genre',
    y='total_audi',
    color='primary_genre',
    hover_name='movieNm',
    points='outliers',
    title="영화 10편 이상 주요 장르별 총 관객수 박스플롯",
    labels={'primary_genre': '장르', 'total_audi': '총 관객수(명)'}
)

fig5.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** 주요 장르별 관객수의 중간값과 편차 범위, 그리고 평균 범위를 뛰어넘는 메가 히트 흥행작(이상치 점)의 위치를 비교할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 6. 개봉일 스크린수 vs 총 관객수 (첫 주 관객 크기의 버블 그래프)
# -------------------------------------------------------------------
st.subheader("6. 개봉일 스크린수, 총 관객수 및 첫 주 관객수 관계 (버블 그래프)")

fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',
    color='primary_genre',
    hover_name='movieNm',
    size_max=40,
    title="개봉일 스크린수 vs 총 관객수 (점 크기: 개봉 첫 주 관객수)",
    labels={
        'first_scrn': '개봉일 스크린수',
        'total_audi': '총 관객수(명)',
        'first_week_audi': '개봉 첫 주 관객수',
        'primary_genre': '장르'
    }
)

fig6.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>개봉일 스크린수: %{x}개<br>총 관객수: %{y:,.0f}명<extra></extra>"
)

st.plotly_chart(fig6, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** 초기 스크린수와 총 관객수 관계에 '첫 주 관객 폭발력' 변수를 추가하여, 초반 흥행 속도까지 종합적으로 비교해 볼 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 7. 제작 국가 및 장르별 영화 편수 (선버스트 그래프)
# -------------------------------------------------------------------
st.subheader("7. 제작 국가 및 장르 계층 구조")

sunburst_df = df.copy()
sunburst_grouped = (
    sunburst_df.groupby(['nation', 'primary_genre'])
    .size()
    .reset_index(name='count')
)

fig7 = px.sunburst(
    sunburst_grouped,
    path=['nation', 'primary_genre'],
    values='count',
    title="제작 국가 -> 장르 계층별 영화 편수 선버스트 차트"
)

fig7.update_traces(
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<extra></extra>"
)

st.plotly_chart(fig7, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** 제작 국가별 영화 생산 비중과 각 국가 내에서 주력을 이루는 영화 장르의 비율 구조를 계층적으로 파악할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 8. 제작 국가별 영화 편수의 비율 (트리맵)
# -------------------------------------------------------------------
st.subheader("8. 제작 국가별 영화 편수의 비율은 어떠한가")

fig8 = px.treemap(
    df,
    path=['nation', 'movieNm'],
    values='total_audi',
    color='nation',
    title="제작 국가별 영화 편수의 비율은 어떠한가"
)

fig8.update_traces(
    hovertemplate="<b>영화명/국가: %{label}</b><br>총 관객수: %{value:,.0f}명<br>비율: %{percentRoot:.1%}<extra></extra>"
)

st.plotly_chart(fig8, use_container_width=True)

st.info("**이 그래프로 알 수 있는 것:** 국가별 전체 관객 시장 규모 비중과 각 국가를 대표하는 개별 영화가 전체 시장에서 차지하는 비율을 한눈에 파악할 수 있습니다.")
