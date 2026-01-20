def get_outfit_suggestion(temp):
    temp = float(temp)
    if temp >= 28:
        return "☀️ 매우 더워요! 민소매와 짧은 반바지를 추천합니다."
    elif 23 <= temp < 28:
        return "👕 반팔 티셔츠와 얇은 면바지가 적당해요."
    elif 17 <= temp < 23:
        return "👔 얇은 가디건이나 긴팔 셔츠를 챙기세요."
    elif 9 <= temp < 17:
        return "🧥 자켓이나 트렌치코트가 필요한 날씨입니다."
    elif 5 <= temp < 9:
        return "🧤 많이 쌀쌀해요. 코트나 가죽 자켓을 입으세요."
    else:
        return "❄️ 한파 주의! 패딩과 목도리로 무장하세요."