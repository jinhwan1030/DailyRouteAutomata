import requests
from datetime import datetime


def get_current_weather(auth_key, nx=73, ny=134):
    # API HUB 초단기실황 엔드포인트
    url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfct_tm.do"

    params = {
        'tm': datetime.now().strftime('%Y%m%d%H%M'),
        'authKey': auth_key,
        'help': '0'
    }

    try:
        response = requests.get(url, params=params)
        # API HUB의 응답 형식에 따라 파싱 로직은 달라질 수 있습니다.
        # 여기서는 성공 여부만 체크하는 기본 구조를 제시합니다.
        if response.status_code == 200:
            return response.text  # 실제 데이터 구조에 맞게 슬라이싱 필요
        return None
    except:
        return None