def get_outfit_suggestion(temp):
    t = float(temp)
    if t >= 28: return "☀️ **[폭염]** 민소매, 반바지, 린넨 소재 옷차림이 필수입니다."
    elif 23 <= t < 28: return "👕 **[더움]** 반팔, 얇은 셔츠를 추천합니다."
    elif 17 <= t < 23: return "👔 **[쾌적]** 얇은 가디건이나 긴팔 티셔츠를 준비하세요."
    elif 9 <= t < 17: return "🧥 **[쌀쌀]** 자켓, 트렌치코트, 야상을 입으세요."
    elif 5 <= t < 9: return "🧣 **[추움]** 코트, 가죽 자켓, 히트텍을 추천합니다."
    else: return "❄️ **[한파]** 패딩, 기모바지, 목도리를 꼭 챙기세요."