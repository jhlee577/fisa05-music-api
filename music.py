import requests
import random
from datetime import datetime

README_PATH = "README.md"

def get_random_song():
    """
    iTunes Search API에서 랜덤 음악 정보를 가져옵니다.
    - 랜덤 키워드를 선택해 검색
    - 결과 중 무작위 곡을 선택
    """
    keywords = ["love", "dance", "jazz", "rock", "lofi", "pop", "kpop", "ballad", "piano", "rap"]
    keyword = random.choice(keywords)
    url = f"https://itunes.apple.com/search?term={keyword}&media=music&country=KR&limit=10"

    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None

        song = random.choice(results)

        return {
            "track": song.get("trackName", "Unknown Track"),
            "artist": song.get("artistName", "Unknown Artist"),
            "album": song.get("collectionName", "Unknown Album"),
            "artwork": song.get("artworkUrl100", ""),
            "preview": song.get("previewUrl", ""),
            "link": song.get("trackViewUrl", "")
        }

    except requests.RequestException as e:
        print("API 요청 오류:", e)
        return None

def update_readme():
    song = get_random_song()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not song:
        content = f"""
# 🎵 Daily Music Recommendation

죄송합니다. 오늘의 추천 곡을 가져오는 데 실패했습니다.

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""
    else:
        content = f"""
# 🎵 Daily Music Recommendation

오늘의 추천 곡은...

## 🎧 {song['track']}  
> 아티스트: **{song['artist']}**  
> 앨범: _{song['album']}_  

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
