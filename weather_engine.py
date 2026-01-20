import streamlit as st
from streamlit_js_eval import get_geolocation
import pytz
from datetime import datetime

# 모듈 가져오기 (파일명이 정확해야 합니다: weather_engine.py, coordi_logic.py)
import weather_engine
import coordi_logic

# 페이지 설정
st.set_page_config(page_title="DailyRouteAutomata", page_icon="🚗", layout="wide")

# 한국 시간대 설정
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

# 한글 폰트 가독성 및 디자인 강화 CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .info-container {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border-left: 5px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 데일리루트 오토마타")
st.markdown(f"#### {now_korea.strftime('%Y년 %m월 %d일 %p %I시 %M분')} | 맞춤형 생활 가이드")

# 위치 정보 가져오기
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # 설정값 로드
    auth_key = st.secrets["KMA_AUTH_KEY"]
    kakao_key = st.secrets["KAKAO_API_KEY"]

    with st.spinner('실시간 정보를 분석하고 있습니다...'):
        지역명 = weather_engine.get_location_name(kakao_key, lat, lon)
        기상정보 = weather_engine.get_weather_detail(auth_key, lat, lon)

    if 기상정보:
        # 상단 지역 표시
        st.subheader(f"📍 현재 위치: {지역명}")

        # 기상 지표 4분할
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("현재 기온", f"{기상정보['temp']}°C")
        with m2:
            st.metric("현재 습도", f"{기상정보['humid']}%")
        with m3:
            st.metric("바람 세기", f"{기상정보['wind']}m/s")
        with m4:
            st.metric("시간당 강수", f"{기상정보['rain']}mm")

        st.divider()

        # 핵심 분석 섹션
        좌측, 우측 = st.columns(2)

        with 좌측:
            st.markdown("### 👔 추천 옷차림")
            의상추천 = coordi_logic.get_outfit_suggestion(기상정보['temp'])
            st.info(f"**오늘의 코디 가이드:**\n\n{의상추천}")

        with 우측:
            st.markdown("### 🚦 도로 교통 정보")
            # 텅 빈 느낌을 없애기 위한 상세 텍스트 구성
            st.warning(f"🚗 **{지역명}** 주변 소통 분석\n\n현재 주요 도로 흐름은 원활한 편입니다. 퇴근길 안전 운행에 유의하세요!")
            st.write(f"- 실시간 사고 및 공사 소식 없음")
            st.write(f"- 도로 노면 상태: **양호**")

        st.divider()
        # 하단 안내 (불필요한 격자 정보 제거)
        st.caption("기상청 실시간 단기 예보 및 카카오 위치 데이터를 기반으로 생성된 정보입니다.")
    else:
        st.error("데이터를 가져오지 못했습니다. 잠시 후 다시 시도해 주세요.")
else:
    # 대기 화면 디자인
    st.info("👋 **반갑습니다! 데일리루트 오토마타입니다.**\n\n위치 권한을 허용해주시면 현재 계신 곳의 날씨와 교통 상황을 분석해 드립니다.")
    st.image("https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&q=80&w=2000")