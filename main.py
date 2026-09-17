import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정

st.set_page_config(
page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
page_icon="🎬",
layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
df = pd.read_csv(DATA_URL)

```
# 장르에 세로막대(|)로 여러 장르가 적혀 있다면 첫 번째 장르만 사용
df["genre"] = df["genre"].fillna("").astype(str).str.split("|").str[0].str.strip()

return df
```

try:
df = load_data()
except Exception as e:
st.error("영화 데이터를 불러오는 중 문제가 발생했습니다.")
st.exception(e)
st.stop()

# 데이터 개요

st.subheader("데이터 살펴보기")
st.write(f"총 **{len(df):,}편**의 영화 데이터를 사용합니다.")

with st.expander("원본 데이터 보기"):
st.dataframe(df, use_container_width=True)

# ---------------------------------------------------------

# 그래프 1. 장르별 영화 편수

# ---------------------------------------------------------

st.divider()
st.header("1. 장르별 영화 편수")

genre_counts = (
df["genre"]
.replace("", "미분류")
.value_counts()
.reset_index()
)

genre_counts.columns = ["genre", "count"]

fig = px.pie(
genre_counts,
names="genre",
values="count",
hole=0.55,
title="장르별 영화 편수",
)

fig.update_traces(
textinfo="percent",
hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
)

fig.update_layout(
legend_title_text="장르",
margin=dict(t=60, b=20, l=20, r=20),
)

st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.write("여기에 장르별 영화 편수와 비율을 보고 알 수 있는 내용을 한 문장으로 적어 보세요.")

# ---------------------------------------------------------

# 이후 그래프를 추가할 때 사용할 구역

# ---------------------------------------------------------

st.divider()
st.header("2. 다음 그래프")

st.info("이곳에 두 번째 그래프를 추가할 수 있습니다.")

with st.container(border=True):
st.markdown("### 💡 이 그래프로 알 수 있는 것")
st.write("여기에 이 그래프를 통해 알 수 있는 내용을 한 문장으로 적어 보세요.")
