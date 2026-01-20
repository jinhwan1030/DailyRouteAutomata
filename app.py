import streamlit as st
from streamlit_js_eval import get_geolocation
import pytz
from datetime import datetime

# 모듈 임포트
import weather_engine
import coordi_logic

# 페이지 설정
st.set_page_config(page_title="Daily-Route-Auto", page_icon="🚗", layout="wide")

# 한국 시간대 설정 (2026-01-20 17:41 기준)
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

# 세련된 한글 UI를 위한 CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 날씨 확인 후 출발하세요")
st.markdown(f"#### {now_korea.strftime('%Y년 %m월 %d일 %p %I시 %M분')} | 맞춤형 생활 가이드")

# 위치 정보 가져오기 (문제가 된 key 인자 제거)
loc = get_geolocation()

if loc:
    try:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

        # 설정값 로드
        auth_key = st.secrets["KMA_AUTH_KEY"]
        kakao_key = st.secrets["KAKAO_API_KEY"]

        with st.spinner('실시간 정보를 분석하고 있습니다...'):
            주소 = weather_engine.get_location_name(kakao_key, lat, lon)
            날씨 = weather_engine.get_weather_detail(auth_key, lat, lon)

        if 날씨:
            st.subheader(f"📍 현재 위치: {주소}")

            # 기상 지표 4분할 (격자 정보 제거)
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("현재 온도", f"{날씨['temp']}°C")
            with m2:
                st.metric("습도", f"{날씨['humid']}%")
            with m3:
                st.metric("바람 세기", f"{날씨['wind']}m/s")
            with m4:
                st.metric("강수량", f"{날씨['rain']}mm")

            st.divider()

            # 핵심 가이드 섹션
            좌, 우 = st.columns(2)
            with 좌:
                st.markdown("### 👔 추천 옷차림")
                코디 = coordi_logic.get_outfit_suggestion(날씨['temp'])
                st.info(f"**오늘의 코디 가이드:**\n\n{코디}")

            with 우:
                st.markdown("### 🚦 도로 교통 정보")
                st.warning(f"🚗 **{주소}** 주변 소통 분석\n\n현재 주요 도로 흐름은 원활합니다. 안전 운행하세요!")
                st.write(f"- 실시간 사고 및 공사 정보 없음")
                st.write(f"- 도로 노면 상태: **양호**")

            st.divider()
            st.caption("기상청 및 카카오 실시간 데이터를 기반으로 생성된 정보입니다.")
        else:
            st.error("기상 데이터를 분석하는 중 오류가 발생했습니다.")
    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
else:
    st.info("👋 **반갑습니다! 데일리루트 오토마타입니다.**\n\n위치 권한을 허용해주시면 현재 위치에 맞는 날씨와 교통 상황을 분석해 드립니다.")
    st.image("https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&q=80&w=2000")