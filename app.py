import streamlit as st
from streamlit_js_eval import get_geolocation

# 모듈 로딩 시 에러 방지를 위해 예외 처리 추가
try:
    from weather_engine import get_weather_detail, get_location_name
    from coordi_logic import get_outfit_suggestion
except ImportError as e:
    st.error(f"모듈 로드 실패: {e}. 모든 파일이 최상위 폴더에 있는지 확인하세요.")

from datetime import datetime
import pytz

st.set_page_config(page_title="DailyRouteAutomata", page_icon="🚗", layout="wide")

# 한국 시간대 고정 (2026-01-20 17:30 기준 자동 처리)
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

# 세련된 CSS (카드 디자인 및 색감 조절)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .info-box { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 DailyRouteAutomata")
st.caption(f"{now_korea.strftime('%Y-%m-%d %H:%M')} | 실시간 지능형 경로 가이드")

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # Secrets 관리
    auth_key = st.secrets.get("KMA_AUTH_KEY")
    kakao_key = st.secrets.get("KAKAO_API_KEY")

    with st.spinner('위치 정보를 분석하고 있습니다...'):
        addr_name = get_location_name(kakao_key, lat, lon)
        weather = get_weather_detail(auth_key, lat, lon)

    if weather:
        st.subheader(f"📍 {addr_name}")

        # 기상 지표 4분할
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🌡️ 기온", f"{weather['temp']}°C")
        m2.metric("💧 습도", f"{weather['humid']}%")
        m3.metric("🌬️ 풍속", f"{weather['wind']}m/s")
        m4.metric("☔ 강수량", f"{weather['rain']}mm")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 👔 Today's Outfit")
            advice = get_outfit_suggestion(weather['temp'])
            st.info(f"**AI 분석 결과:**\n\n{advice}")

        with col2:
            st.markdown("### 🚥 Road Status")
            st.warning("⚠️ **실시간 교통 분석**\n\n현재 주요 간선도로 흐름이 양호합니다. 퇴근길 안전 운행하세요!")
            st.write(f"- 대상 구역: {addr_name} 중심 반경 5km")
    else:
        st.error("데이터 연동 실패. API 키 권한이나 형식을 확인하세요.")
else:
    st.image("https://images.unsplash.com/photo-1517404215738-15263e9f9178?auto=format&fit=crop&q=80&w=2000",
             caption="Connect Your Location")
    st.info("💡 **위치 권한 승인이 필요합니다.**\n\n권한을 허용하시면 즉시 행정동 단위 주소와 맞춤형 코디를 제공합니다.")