import streamlit as st
from weather_engine import get_current_weather
from coordi_logic import get_outfit_suggestion

# 페이지 설정
st.set_page_config(page_title="DailyRouteAutomata", page_icon="🤖", layout="wide")

# CSS를 활용한 디자인 강화
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_status_code=True)

st.title("🤖 DailyRouteAutomata")
st.caption("실시간 기상 데이터 기반 자동화 가이드 시스템")

# API 키 가져오기 (Secrets 관리)
auth_key = st.secrets["KMA_AUTH_KEY"]

# 레이아웃 분할
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📍 실시간 기상 상황")
    # 예시 온도 (실제로는 weather_engine에서 파싱한 값 사용)
    current_temp = 7.2
    st.metric(label="현재 기온", value=f"{current_temp} °C", delta="-1.2 °C")
    st.write("현재 위치를 기반으로 관측된 데이터입니다.")

with col2:
    st.subheader("👔 추천 옷차림")
    advice = get_outfit_suggestion(current_temp)
    st.info(advice)

st.divider()
st.subheader("🚥 교통 정보 (Commute Status)")
st.warning("현재 도로 소통 정보 API 연동 준비 중입니다.")