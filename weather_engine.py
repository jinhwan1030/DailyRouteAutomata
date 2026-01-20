import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def get_weather_data(auth_key, lat, lon):
    # 좌표 변환 로직 (실제 기상청 격자 좌표 nx, ny 변환 필요)
    # 여기서는 예시로 고정 좌표를 사용하거나 변환 함수를 추가할 수 있습니다.
    nx, ny = 73, 134  # 춘천 기준 예시

    url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'XML',
        'base_date': datetime.now().strftime('%Y%m%d'),
        'base_time': datetime.now().strftime('%H00'),
        'nx': nx,
        'ny': ny,
        'authKey': auth_key
    }

    try:
        response = requests.get(url, params=params)
        root = ET.from_those(response.content)

        # XML 데이터 파싱
        weather_dict = {}
        for item in root.findall('.//item'):
            category = item.find('category').text
            value = item.find('obsrValue').text
            weather_dict[category] = value

        return {
            'temp': weather_dict.get('T1H', '0'),
            'humidity': weather_dict.get('REH', '0'),
            'rain': weather_dict.get('RN1', '0'),
            'base_time': params['base_time']
        }
    except:
        return None