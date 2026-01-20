import streamlit as st
from streamlit_js_eval import get_geolocation
from weather_engine import get_weather_detail, get_location_name
from coordi_logic import get_outfit_suggestion
from datetime import datetime
import pytz

# 페이지 설정 및 테마
st.set_page_config(page_title="DailyRouteAutomata", page_icon="🚗", layout="wide")

# 고도화된 CSS 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto+Sans+KR', sans-serif; }
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .stAlert { border-radius: 15px; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .metric-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.08); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 한국 시간 설정
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

# 메인 헤더
st.title("🚗 DailyRouteAutomata")
st.markdown(f"**{now_korea.strftime('%m월 %d일 %A')}** | 실시간 개인화 이동 가이드")

# 위치 정보 획득
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # API 키 로드
    auth_key = st.secrets["KMA_AUTH_KEY"]
    kakao_key = st.secrets["KAKAO_API_KEY"]

    # 1. 지역명 및 날씨 데이터 가져오기
    addr_name = get_location_name(kakao_key, lat, lon)
    weather_data = get_weather_detail(auth_key, lat, lon)

    if weather_data:
        # 상단 섹션: 현재 위치 및 주요 지표
        st.subheader(f"📍 {addr_name}")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("🌡️ 기온", f"{weather_data['temp']}°C")
        with m2:
            st.metric("💧 습도", f"{weather_data['humid']}%")
        with m3:
            st.metric("🌬️ 풍속", f"{weather_data['wind']}m/s")
        with m4:
            st.metric("☔ 강수량", f"{weather_data['rain']}mm")

        st.divider()

        # 중앙 섹션: 코디 & 교통 (핵심 가치)
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 👔 Today's Outfit")
            advice = get_outfit_suggestion(weather_data['temp'])
            st.success(f"**AI 추천 코디:**\n\n{advice}")

        with col2:
            st.markdown("### 🚥 Traffic Status")
            # 춘천(또는 현재지역) 기반 가상 데이터 (추후 API 연동)
            st.warning("🚗 **실시간 교통 분석**\n\n주요 출퇴근 경로에 정체가 감지되지 않습니다. 평소대로 출발하세요.")

        st.divider()

        # 하단 섹션: 상세 분석 요약
        with st.expander("📊 상세 기상 분석 데이터 확인"):
            st.write(f"- 관측 시간: {now_korea.strftime('%H:%M')} KST")
            st.write(f"- 풍향: {weather_data['vec']}도 방향")
            st.progress(int(float(weather_data['humid'])) / 100, text="현재 습도 수준")

    else:
        st.error("기상 데이터를 불러오는 중 오류가 발생했습니다. 잠시 후 새로고침 해주세요.")
else:
    st.info("👋 **안녕하세요! DailyRouteAutomata입니다.**\n\n좌측 상단(또는 팝업)의 위치 정보 권한을 허용해 주시면, 계신 곳의 날씨와 교통 상황을 자동으로 분석해 드립니다.")
    # 대표 이미지 배치 (텅 빈 느낌 방지)
    st.image("https://images.unsplash.com/photo-1496247749665-49cf94d99ee6?auto=format&fit=crop&q=80&w=2073",
             caption="Your Journey, Our Automata.")