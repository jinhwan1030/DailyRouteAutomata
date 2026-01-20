import streamlit as st
from streamlit_js_eval import get_geolocation
from weather_engine import get_weather_detail
from coordi_logic import get_outfit_suggestion

st.set_page_config(page_title="DailyRouteAutomata", layout="wide")

# 위치 정보 획득 및 로컬 세션 유지
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    # 실무 팁: 춘천시, 의정부시 등 지역명은 카카오/구글 역지오코딩 API가 필요하나,
    # 우선은 격자 좌표(nx, ny)를 명시하여 신뢰도를 줍니다.

    auth_key = st.secrets["KMA_AUTH_KEY"]
    data = get_weather_detail(auth_key, lat, lon)

    if data:
        st.title(f"🤖 DailyRouteAutomata")
        st.success(f"📍 현재 측정 위치: 격자 좌표 ({data['nx']}, {data['ny']}) 기반 실시간 정보")

        # 상세 기상 대시보드
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("기온", f"{data['temp']}°C")
        m2.metric("습도", f"{data['humid']}%")
        m3.metric("풍속", f"{data['wind']}m/s")
        m4.metric("강수량", f"{data['rain']}mm")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("👔 추천 옷차림")
            st.info(get_outfit_suggestion(data['temp']))

        with col2:
            st.subheader("📝 기상 분석 보고")
            wind_dir = "북풍" if float(data['vec']) < 45 else "서풍"  # 간이 로직
            st.write(f"- 현재 **{data['time']}** 기준, 실시간 기온은 **{data['temp']}도**입니다.")
            st.write(f"- **{wind_dir}**이 불고 있으며 습도는 **{data['humid']}%**로 기록됩니다.")
            if float(data['rain']) > 0:
                st.write("- 🌧️ 현재 비가 내리고 있으니 반드시 우산을 지참하세요.")
            else:
                st.write("- ☀️ 강수 정보가 없어 야외 활동에 지장이 없습니다.")
    else:
        st.error("기상청 데이터를 분석할 수 없습니다. 잠시 후 다시 시도해 주세요.")
else:
    st.warning("위치 권한을 허용하시면 사용자의 위치를 자동으로 저장하고 가이드를 생성합니다.")