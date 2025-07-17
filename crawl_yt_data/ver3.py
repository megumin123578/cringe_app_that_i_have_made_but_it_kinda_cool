from googleapiclient.discovery import build
from datetime import datetime
import pytz
import pandas as pd

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

# Test
handles = ["Moeiau","chimvandaycot9534","daylaphegame", "tinhte" ]
for chanel in handles:
    info = get_latest_videos_info(chanel, 50)

    if info:
        print("Channel Name:", info["channel_name"])
        print("Danh sách video mới nhất:")
        for idx, v in enumerate(info["videos"], start=1):
            print(f"{idx}. {v['title']} ({v['published_at']}) - Views: {v['view_count']} Likes: {v['like_count']}")
    else:
        print("Không tìm thấy channel!")
