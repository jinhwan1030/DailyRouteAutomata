import streamlit as st
from streamlit_js_eval import get_geolocation
from weather_engine import get_weather_data
from coordi_logic import get_outfit_suggestion

# 페이지 설정
st.set_page_config(page_title="DailyRouteAutomata", page_icon="🤖", layout="wide")

# CSS 스타일 적용 (unsafe_allow_html=True로 수정 완료)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 DailyRouteAutomata")
st.caption("실시간 기상 및 교통 데이터 기반 무인 가이드 시스템")

# 1. 위치 정보 획득
with st.sidebar:
    st.header("📍 Location Setting")
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        st.success(f"위치 감지 완료: {lat:.2f}, {lon:.2f}")
    else:
        st.warning("위치 권한을 허용해주세요. (기본값: 춘천)")
        lat, lon = 37.88, 127.73  # 기본 좌표

# 2. 데이터 엔진 구동 (API HUB 호출)
auth_key = st.secrets["KMA_AUTH_KEY"]
weather_info = get_weather_data(auth_key, lat, lon)

if weather_info:
    # 3. UI 레이아웃
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📡 실시간 현황 ({weather_info['base_time']} 기준)")
        st.metric("현재 기온", f"{weather_info['temp']}°C")
        st.write(f"습도: {weather_info['humidity']}% | 강수량: {weather_info['rain']}mm")

    with col2:
        st.subheader("👔 AI 코디 추천")
        advice = get_outfit_suggestion(weather_info['temp'])
        st.info(advice)

    st.divider()
    st.subheader("🚥 실시간 교통 상황 (DailyRoute Flow)")
    st.info("현재 주요 도로 흐름을 분석 중입니다. 곧 서비스 예정입니다.")
else:
    st.error("데이터를 불러오는 중입니다. 잠시만 기다려주세요.")