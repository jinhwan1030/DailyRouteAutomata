import streamlit as st
from streamlit_js_eval import get_geolocation
import pytz
from datetime import datetime

# 모듈 임포트 시 예외 처리 강화
try:
    from weather_engine import get_weather_detail, get_location_name
    from coordi_logic import get_outfit_suggestion
except ImportError as e:
    st.error(f"파일 로드 오류: {e}. 모든 .py 파일이 GitHub 최상위 폴더에 있는지 확인하세요.")

st.set_page_config(page_title="DailyRouteAutomata", page_icon="🚗", layout="wide")

# 한국 표준시 설정
KST = pytz.timezone('Asia/Seoul')
now_korea = datetime.now(KST)

st.title("🚗 DailyRouteAutomata")
st.markdown(f"**{now_korea.strftime('%Y-%m-%d %H:%M')}** | 실시간 지능형 라이프 가이드")

# 브라우저 위치 정보 획득
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # Secrets 관리 (Streamlit Cloud 설정에서 입력 필요)
    auth_key = st.secrets["KMA_AUTH_KEY"]
    kakao_key = st.secrets["KAKAO_API_KEY"]

    with st.spinner('실시간 기상 및 위치 정보를 분석 중입니다...'):
        addr_name = get_location_name(kakao_key, lat, lon)
        weather = get_weather_detail(auth_key, lat, lon)

    if weather:
        st.subheader(f"📍 {addr_name}")

        # 4분할 기상 대시보드
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🌡️ 기온", f"{weather['temp']}°C")
        m2.metric("💧 습도", f"{weather['humid']}%")
        m3.metric("🌬️ 풍속", f"{weather['wind']}m/s")
        m4.metric("☔ 강수량", f"{weather['rain']}mm")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 👔 AI Outfit Suggestion")
            advice = get_outfit_suggestion(weather['temp'])
            st.info(f"**추천 스타일:**\n\n{advice}")

        with col2:
            st.markdown("### 🚥 Traffic Status")
            st.warning(f"🚗 **{addr_name}** 주변 도로 상황 분석 중...")
            st.write("- 현재 주요 간선도로 소통이 원활합니다.")
            st.write("- 퇴근 시간대 정체 구간을 확인하세요.")
    else:
        st.error("기상 데이터를 불러오는 중 오류가 발생했습니다. API 키 권한을 확인하세요.")
else:
    st.image("https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&q=80&w=2000")
    st.info("💡 **위치 권한 승인이 필요합니다.**\n\n권한을 허용하시면 현재 위치에 맞는 행정동 주소와 맞춤 날씨 가이드가 즉시 생성됩니다.")