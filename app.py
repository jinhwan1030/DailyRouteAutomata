import streamlit as st
from streamlit_js_eval import get_geolocation
from weather_engine import get_weather_detail, get_location_name
from coordi_logic import get_outfit_suggestion
from datetime import datetime
import pytz

# 프로젝트 설정
st.set_page_config(page_title="DailyRouteAutomata", page_icon="🤖", layout="wide")

# 한국 시간대 설정
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

# CSS 스타일 적용
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 DailyRouteAutomata")

# 위치 정보 획득
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # Secrets에서 키 로드
    auth_key = st.secrets["KMA_AUTH_KEY"]
    kakao_key = st.secrets["KAKAO_API_KEY"]

    # 1. 지역명 및 날씨 데이터 가져오기
    addr_name = get_location_name(kakao_key, lat, lon)
    data = get_weather_detail(auth_key, lat, lon)

    if data:
        st.subheader(f"📍 {addr_name} 실시간 가이드")
        st.caption(f"데이터 업데이트: {now_korea.strftime('%Y-%m-%d %H:%M')} (KST)")

        # 4분할 대시보드
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("현재 기온", f"{data['temp']}°C")
        m2.metric("습도", f"{data['humid']}%")
        m3.metric("풍속", f"{data['wind']}m/s")
        m4.metric("강수량", f"{data['rain']}mm")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("👔 AI 코디 추천")
            st.info(get_outfit_suggestion(data['temp']))

        with col2:
            st.subheader("📝 기상 분석 보고")
            if float(data['rain']) > 0:
                st.warning("☔ 현재 비/눈이 감지되었습니다. 외출 시 우산을 꼭 챙기세요!")
            else:
                st.success("☀️ 현재 강수 정보가 없습니다. 가벼운 외출이 가능합니다.")

            st.write(f"- 현재 습도가 **{data['humid']}%**로 기록되어 쾌적도를 확인하세요.")
    else:
        st.error("기상 데이터를 불러오는 중입니다. API 키를 확인해주세요.")
else:
    st.warning("위치 권한을 허용하시면 현재 계신 곳의 행정구역 정보를 자동으로 불러옵니다.")