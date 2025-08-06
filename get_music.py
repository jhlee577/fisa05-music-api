import requests
import random
from datetime import datetime

README_PATH = "README.md"

# 장르 키워드 리스트 (검색용 term에 사용)
genre_keywords = [
    "kpop", "pop", "hiphop", "ballad", "jazz",
    "acoustic", "rock", "lofi", "instrumental", "rnb"
]

# 분위기나 테마 키워드
mood_keywords = [
    "love", "sad", "happy", "summer", "night", "rain", "dream", "hope"
]

# ISO 국가 코드 목록 (KR, JP, US 등)
country_codes = ["KR", "JP", "US", "GB", "FR", "DE"]

def get_random_song():
    """장르/국가/키워드를 조합해 iTunes API에서 랜덤 곡 가져오기"""

    # 조합 생성
    genre = random.choice(genre_keywords)
    mood = random.choice(mood_keywords)
    keyword = f"{genre}+{mood}"

    country = random.choice(country_codes)

    # API URL 구성
    url = f"https://itunes.apple.com/search?term={keyword}&media=music&country={country}&limit=10"

    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None, country, keyword

        song = random.choice(results)

        return {
            "track": song.get("trackName", "Unknown Track"),
            "artist": song.get("artistName", "Unknown Artist"),
            "album": song.get("collectionName", "Unknown Album"),
            "artwork": song.get("artworkUrl100", ""),
            "preview": song.get("previewUrl", ""),
            "link": song.get("trackViewUrl", "")
        }, country, keyword

    except requests.RequestException as e:
        print("API 요청 오류:", e)
        return None, country, keyword

def update_readme():
    song, country, keyword = get_random_song()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not song:
        content = f"""
# 🎵 Daily Music Recommendation

죄송합니다. 추천 곡을 가져오는 데 실패했습니다.  
조합: `{keyword}` | 국가: `{country}`

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""
    else:
        content = f"""
# 🎵 Music Recommendation

추천 곡은...

## 🎧 {song['track']}  
> 아티스트: **{song['artist']}**  
> 앨범: _{song['album']}_  

🔍 검색 키워드: `{keyword}`  
🌎 국가 스토어: `{country}`

[🔗 iTunes에서 보기]({song['link']})  
{f"[▶️ 미리 듣기]({song['preview']})" if song['preview'] else ''}

![앨범 아트워크]({song['artwork']})

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_readme()