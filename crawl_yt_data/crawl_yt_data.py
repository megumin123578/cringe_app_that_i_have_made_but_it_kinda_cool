from googleapiclient.discovery import build
from datetime import datetime
import pytz
import pandas as pd
import os

def convert_time(iso_time):
    utc_time = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    local_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    local_time = utc_time.astimezone(local_tz)

    return local_time.strftime("%Y-%m-%d %H:%M:%S")

API_KEY = "AIzaSyCXe_Hus2o51PaTBcUVgNDZXHCC81qAJFM"
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_latest_videos_info(handle, max_results=10):
    # 1. Lấy channelId và uploads playlist từ handle
    channel_request = youtube.channels().list(
        part="snippet,contentDetails",
        forHandle=f"@{handle}"
    )
    channel_response = channel_request.execute()

    if not channel_response["items"]:
        return None

    channel = channel_response["items"][0]
    channel_name = channel["snippet"]["title"]
    uploads_playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2. Lấy danh sách video mới nhất
    playlist_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_playlist,
        maxResults=max_results
    )
    playlist_response = playlist_request.execute()

    video_ids = []
    videos = []
    for item in playlist_response["items"]:
        video_id = item["contentDetails"]["videoId"]
        title = item["snippet"]["title"]
        published_at = convert_time(item["snippet"]["publishedAt"])
        video_ids.append(video_id)
        videos.append({
            "video_id": video_id,
            "title": title,
            "published_at": published_at
        })

    # 3. Lấy thông tin view & like cho tất cả video cùng lúc
    video_request = youtube.videos().list(
        part="statistics",
        id=",".join(video_ids)
    )
    video_response = video_request.execute()

    stats_map = {item["id"]: item["statistics"] for item in video_response["items"]}

    for v in videos:
        stats = stats_map.get(v["video_id"], {})
        v["view_count"] = stats.get("viewCount", "0")
        v["like_count"] = stats.get("likeCount", "0")

    return {
        "channel_name": channel_name,
        "videos": videos
    }


handles = ["Moeiau","chimvandaycot9534","daylaphegame", "tinhte" ]
all_data = []

for channel in handles:
    info = get_latest_videos_info(channel, 50)

    if info:
        for v in info["videos"]:
            all_data.append({
                "channel_name": info["channel_name"],
                "video_title": v["title"],
                "published_at": v["published_at"],
                "view_count": v["view_count"],
                "like_count": v["like_count"]
            })
    else:
        print(f"Không tìm thấy channel: {channel}")

# Convert to DataFrame
df = pd.DataFrame(all_data)

os.remove("latest_videos.csv") #clear before save
# Save to CSV
df.to_csv("latest_videos.csv", index=False, encoding="utf-8-sig")

print("Data saved to latest_videos.csv")