import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import math


# 기상청 공식: 위경도 -> 격자 좌표 변환
def convert_to_grid(lat, lon):
    RE, GRID, SLAT1, SLAT2, OLON, OLAT, XO, YO = 6371.00877, 5.0, 30.0, 60.0, 126.0, 38.0, 43, 136
    DEGRAD = math.pi / 180.0
    re = RE / GRID
    slat1, slat2, olon, olat = SLAT1 * DEGRAD, SLAT2 * DEGRAD, OLON * DEGRAD, OLAT * DEGRAD
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(
        math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5))
    sf = math.pow(math.tan(math.pi * 0.25 + slat1 * 0.5), sn) * math.cos(slat1) / sn
    ro = re * sf / math.pow(math.tan(math.pi * 0.25 + olat * 0.5), sn)
    ra = re * sf / math.pow(math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5), sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi: theta -= 2.0 * math.pi
    if theta < -math.pi: theta += 2.0 * math.pi
    theta *= sn
    nx = math.floor(ra * math.sin(theta) + XO + 0.5)
    ny = math.floor(ro - ra * math.cos(theta) + YO + 0.5)
    return nx, ny


def get_weather_detail(auth_key, lat, lon):
    nx, ny = convert_to_grid(lat, lon)
    url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        'pageNo': '1', 'numOfRows': '1000', 'dataType': 'XML',
        'base_date': datetime.now().strftime('%Y%m%d'),
        'base_time': datetime.now().strftime('%H00'),
        'nx': nx, 'ny': ny, 'authKey': auth_key
    }

    try:
        res = requests.get(url, params=params)
        root = ET.fromstring(res.content)
        items = {item.find('category').text: item.find('obsrValue').text for item in root.findall('.//item')}

        # 상세 데이터 매핑
        return {
            'temp': items.get('T1H'),
            'rain': items.get('RN1'),
            'humid': items.get('REH'),
            'wind': items.get('WSD'),
            'vec': items.get('VEC'),
            'nx': nx, 'ny': ny,
            'time': params['base_time']
        }
    except:
        return None