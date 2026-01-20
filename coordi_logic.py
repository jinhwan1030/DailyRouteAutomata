def get_outfit_suggestion(temp):
    t = float(temp)
    if t >= 28: return "☀️ **[무더위]** 민소매, 반팔, 반바지 등 시원한 차림"
    elif 23 <= t < 28: return "👕 **[더움]** 반팔, 얇은 셔츠, 면바지"
    elif 17 <= t < 23: return "👔 **[쾌적]** 얇은 가디건, 긴팔 티셔츠, 청바지"
    elif 9 <= t < 17: return "🧥 **[쌀쌀]** 자켓, 야상, 트렌치코트, 니트"
    elif 5 <= t < 9: return "🧣 **[추움]** 코트, 가죽 자켓, 히트텍, 목도리"
    else: return "❄️ **[한파]** 패딩, 기모바지, 장갑으로 무장하세요!"