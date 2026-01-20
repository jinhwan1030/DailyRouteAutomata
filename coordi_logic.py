def get_outfit_suggestion(temp):
    t = float(temp)
    if t >= 28: return "☀️ **[폭염]** 민소매, 반팔, 반바지, 린넨 소재"
    elif 23 <= t < 28: return "👕 **[더움]** 반팔, 얇은 셔츠, 반바지, 면바지"
    elif 17 <= t < 23: return "👔 **[쾌적]** 얇은 가디건, 긴팔 티, 청바지"
    elif 9 <= t < 17: return "🧥 **[쌀쌀]** 자켓, 트렌치코트, 야상, 니트"
    elif 5 <= t < 9: return "🧣 **[추움]** 코트, 가죽 자켓, 히트텍, 기모바지"
    else: return "❄️ **[한파]** 패딩, 두꺼운 코트, 목도리, 귀도리"