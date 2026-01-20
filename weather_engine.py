import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import math
import pytz


def convert_to_grid(lat, lon):
    """위경도를 기상청 격자 좌표(nx, ny)로 변환"""
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


def get_location_name(kakao_key, lat, lon):
    url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={lon}&y={lat}"
    headers = {"Authorization": f"KakaoAK {kakao_key}"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            doc = res.json()['documents']
            # 행정동 주소가 없을 경우 전체 주소로 대체
            return doc[0]['address_name'] if doc else "위치 식별 불가"
        return "API 호출 오류"
    except:
        return "위치 정보 접근 불가"


def get_weather_detail(auth_key, lat, lon):
    nx, ny = convert_to_grid(lat, lon)
    KST = pytz.timezone('Asia/Seoul')
    now_korea = datetime.now(KST)

    url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        'pageNo': '1', 'numOfRows': '1000', 'dataType': 'XML',
        'base_date': now_korea.strftime('%Y%m%d'),
        'base_time': now_korea.strftime('%H00'),
        'nx': nx, 'ny': ny, 'authKey': auth_key
    }

    try:
        res = requests.get(url, params=params)
        root = ET.fromstring(res.content)
        items = {item.find('category').text: item.find('obsrValue').text for item in root.findall('.//item')}
        return {
            'temp': items.get('T1H'),
            'rain': items.get('RN1'),
            'humid': items.get('REH'),
            'wind': items.get('WSD'),
            'vec': items.get('VEC')
        }
    except:
        return None