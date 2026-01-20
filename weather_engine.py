import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def get_weather_data(auth_key, lat, lon):
    # 기상청 격자 좌표 변환 (간이 로직: 춘천 기준 73, 134)
    # 실제 운영 시 위도/경도를 nx, ny로 변환하는 공식 함수가 필요합니다.
    nx, ny = 73, 134

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
        root = ET.fromstring(response.content)

        data_dict = {}
        for item in root.findall('.//item'):
            category = item.find('category').text
            value = item.find('obsrValue').text
            data_dict[category] = value

        return {
            'temp': data_dict.get('T1H', '0'),
            'humidity': data_dict.get('REH', '0'),
            'rain': data_dict.get('RN1', '0'),
            'base_time': params['base_time'],
            'location_name': "사용자 근처 측정소"
        }
    except Exception as e:
        print(f"Error: {e}")
        return None