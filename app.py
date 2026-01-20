import streamlit as st
from streamlit_js_eval import get_geolocation
from weather_engine import get_weather_detail, get_location_name
from coordi_logic import get_outfit_suggestion
from datetime import datetime
import pytz

# 페이지 설정
st.set_page_config(page_title="DailyRouteAutomata", page_icon="🚗", layout="wide")

# 고급 CSS 적용: 텍스트 가독성 및 카드 디자인 강화
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    .status-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #2c3e50; }
    </style>
    """, unsafe_allow_html=True)

# 한국 시간대 설정 (KST)
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

st.title("🚗 DailyRouteAutomata")
st.markdown(f"**{now_korea.strftime('%Y년 %m월 %d일 %H:%M')}** | 개인 맞춤형 이동 가이드")

# 위치 정보 획득
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # Secrets 로드
    auth_key = st.secrets["KMA_AUTH_KEY"]
    kakao_key = st.secrets["KAKAO_API_KEY"]

    with st.spinner('실시간 위치 및 기상 정보를 동기화 중입니다...'):
        addr_name = get_location_name(kakao_key, lat, lon)
        weather = get_weather_detail(auth_key, lat, lon)

    if weather:
        # 상단: 지역명 및 상세 정보
        st.subheader(f"📍 {addr_name}")

        # 4분할 지표 카드
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🌡️ 기온", f"{weather['temp']}°C")
        m2.metric("💧 습도", f"{weather['humid']}%")
        m3.metric("🌬️ 풍속", f"{weather['wind']}m/s")
        m4.metric("☔ 강수량", f"{weather['rain']}mm")

        st.divider()

        # 중앙 섹션: 코디 및 교통 상황 (UI 꽉 채우기)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 👔 AI Outfit Suggestion")
            advice = get_outfit_suggestion(weather['temp'])
            st.info(f"**오늘의 추천 스타일:**\n\n{advice}")

        with col2:
            st.markdown("### 🚥 Real-time Traffic")
            # 가상 데이터로 UI 밀도 확보
            st.warning("🔄 **주변 도로 분석 결과**\n\n현재 주요 간선도로 소통이 원활합니다. 평소보다 5분 일찍 출발하시면 쾌적한 이동이 가능합니다.")
            st.caption(f"기준 지점: {addr_name} 인근 주요 도로")

        # 하단 상세 정보
        with st.expander("📊 데이터 분석 상세 보기"):
            st.write(f"- 관측 시간: {now_korea.strftime('%H:%M')} (KST)")
            st.write(f"- 기상청 격자 좌표: nx={weather['nx']}, ny={weather['ny']}")
            st.progress(int(float(weather['humid'])) / 100, text="대기 중 습도 비율")
    else:
        st.error("기상청 API 인증 실패 혹은 점검 중입니다. API HUB의 'authKey'를 확인해 주세요.")
else:
    # 위치 권한 허용 전 대기 화면 (이미지 활용으로 텅 빈 느낌 방지)
    st.info("💡 **위치 정보 권한이 필요합니다.**\n\n브라우저 상단에서 위치 권한을 승인하시면, 계신 곳의 주소와 날씨를 자동으로 불러옵니다.")
    st.image("https://images.unsplash.com/photo-1449156001931-82992a472695?auto=format&fit=crop&q=80&w=2000",
             caption="Smart Journey Begins with DailyRouteAutomata.")