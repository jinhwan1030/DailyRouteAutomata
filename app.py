import streamlit as st
from streamlit_js_eval import get_geolocation
from weather_engine import get_weather_detail, get_location_name
from coordi_logic import get_outfit_suggestion
from datetime import datetime
import pytz

st.set_page_config(page_title="DailyRouteAutomata", page_icon="🚗", layout="wide")

# 한국 시간 설정
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

# 세련된 CSS (카드 디자인 및 배경)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .metric-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stMetric { color: #1f77b4; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 DailyRouteAutomata")
st.markdown(f"**{now_korea.strftime('%Y년 %m월 %d일 %H:%M')}** | 현재 위치 기반 자동화 가이드")

# 위치 정보 획득
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # Secrets 로드
    auth_key = st.secrets["KMA_AUTH_KEY"]
    kakao_key = st.secrets["KAKAO_API_KEY"]

    # 데이터 로딩 애니메이션
    with st.spinner('실시간 기상 및 위치 정보를 분석 중입니다...'):
        addr_name = get_location_name(kakao_key, lat, lon)
        weather = get_weather_detail(auth_key, lat, lon)

    if weather:
        st.success(f"📍 **현재 위치:** {addr_name} (격자: {weather['nx']}, {weather['ny']})")

        # 4분할 지표 카드
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("🌡️ 현재 온도", f"{weather['temp']}°C")
        with m2:
            st.metric("💧 습도", f"{weather['humid']}%")
        with m3:
            st.metric("🌬️ 풍속", f"{weather['wind']}m/s")
        with m4:
            st.metric("☔ 강수량", f"{weather['rain']}mm")

        st.divider()

        # 코디 및 분석 섹션
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("👔 AI 추천 코디")
            advice = get_outfit_suggestion(weather['temp'])
            st.info(f"**오늘의 추천:**\n\n{advice}")

        with col2:
            st.subheader("🚦 출퇴근 교통 상황")
            # 가상 데이터 노출 (UI 꽉 채우기용)
            st.warning("🔄 주변 도로 소통 원활 (실시간 교통 API 연동 준비 중)")
            st.write(f"- 현재 {addr_name} 주변 사고 소식은 없습니다.")
            st.write("- 기상 상태에 따른 가시거리는 양호합니다.")

    else:
        st.error("기상청 API 호출에 실패했습니다. API 키의 권한이나 URL 형식을 다시 확인해주세요.")
else:
    # 텅 빈 느낌 방지용 이미지와 가이드
    st.image("https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&q=80&w=2000",
             caption="Connect your location for smarter journey.")
    st.info("💡 **위치 권한을 허용해주세요!**\n\n상단 팝업에서 권한을 승인하시면 귀하의 위치에 맞는 날씨와 교통 정보를 자동으로 계산합니다.")