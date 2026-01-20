import streamlit as st
from streamlit_js_eval import get_geolocation
from weather_engine import get_weather_data
from coordi_logic import get_outfit_suggestion

# 페이지 설정
st.set_page_config(page_title="DailyRouteAutomata", page_icon="🤖", layout="wide")

# CSS 스타일 (오타 수정 버전)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 DailyRouteAutomata")

# 1. 위치 정보 획득 (브라우저 기반)
loc = get_geolocation()

if loc:
    lat = loc['coords']['latitude']
    lon = loc['coords']['longitude']

    # 2. 데이터 호출 (기상청 API HUB)
    auth_key = st.secrets["KMA_AUTH_KEY"]
    weather = get_weather_data(auth_key, lat, lon)

    if weather:
        st.success(f"📡 현재 측정 지역: {weather['location_name']} (기준 시간: {weather['base_time']})")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("현재 기온", f"{weather['temp']}°C")
            st.write(f"습도: {weather['humidity']}% | 1시간 강수량: {weather['rain']}mm")

        with col2:
            st.subheader("👔 AI 코디 추천")
            advice = get_outfit_suggestion(weather['temp'])
            st.info(advice)
    else:
        st.error("기상 데이터를 불러오는 데 실패했습니다. API 키와 네트워크 상태를 확인하세요.")
else:
    st.warning("위치 권한을 허용하시면 현재 계신 곳의 맞춤형 가이드를 자동으로 생성합니다.")
    st.info("권한 허용 후 잠시 기다려주시거나 페이지를 새로고침 해주세요.")

st.divider()
st.subheader("🚥 DailyRoute Flow (교통 상황)")
st.info("실시간 교통 데이터 연동 준비 중입니다.")