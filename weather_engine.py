import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import math
import pytz


def get_location_name(kakao_key, lat, lon):
    """카카오 API: 위경도 -> 행정구역 명칭 (일일 30만건 무료)"""
    url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={lon}&y={lat}"
    headers = {"Authorization": f"KakaoAK {kakao_key}"}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            doc = res.json().get('documents', [])
            return doc[0]['address_name'] if doc else "위치 정보 없음"
        return f"API 오류({res.status_code})"
    except:
        return "연결 실패"


def convert_to_grid(lat, lon):
    """기상청 공식 위경도 -> 격자(nx, ny) 변환"""
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
    KST = pytz.timezone('Asia/Seoul')
    now = datetime.now(KST)

    # 초단기실황 API URL (사용자 제공 형식 반영)
    url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtNcst"
    params = {
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'XML',
        'base_date': now.strftime('%Y%m%d'),
        'base_time': now.strftime('%H00'),
        'nx': str(nx),
        'ny': str(ny),
        'authKey': auth_key
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            # 결과 코드 확인 (00: 정상)
            res_code = root.find('.//resultCode')
            if res_code is not None and res_code.text == '00':
                items = {item.find('category').text: item.find('obsrValue').text for item in root.findall('.//item')}
                return {
                    'temp': items.get('T1H', '0'),
                    'rain': items.get('RN1', '0'),
                    'humid': items.get('REH', '0'),
                    'wind': items.get('WSD', '0'),
                    'nx': nx, 'ny': ny
                }
        return None
    except:
        return None