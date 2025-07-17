from googleapiclient.discovery import build
from datetime import datetime
import pytz

def convert_time(iso_time):
    utc_time = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    local_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    local_time = utc_time.astimezone(local_tz)

    return local_time.strftime("%Y-%m-%d %H:%M:%S").split(' ')

API_KEY = "AIzaSyCXe_Hus2o51PaTBcUVgNDZXHCC81qAJFM"
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_latest_video_info(handle):
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
    channel_id = channel["id"]
    uploads_playlist = channel["contentDetails"]["relatedPlaylists"]["uploads"]

    # 2. Lấy video mới nhất từ uploads playlist
    playlist_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_playlist,
        maxResults=1
    )
    playlist_response = playlist_request.execute()

    latest_item = playlist_response["items"][0]
    latest_video_id = latest_item["contentDetails"]["videoId"]
    latest_video_title = latest_item["snippet"]["title"]
    published_at = latest_item["snippet"]["publishedAt"]

    # 3. Lấy thông tin chi tiết của video
    video_request = youtube.videos().list(
        part="snippet,statistics",
        id=latest_video_id
    )
    video_response = video_request.execute()
    video_info = video_response["items"][0]
    view_count = video_info["statistics"].get("viewCount", "0")

    return {
        "channel_name": channel_name,
        "channel_id": channel_id,
        "video_id": latest_video_id,
        "title": latest_video_title,
        "published_at": published_at,
        "view_count": view_count
    }

# Test hàm
handle = "chimvandaycot9534"  # không cần thêm @ vì code đã thêm
info = get_latest_video_info(handle)

if info:
    print("Channel Name:", info["channel_name"])
    print("Channel ID:", info["channel_id"])
    print("Latest Video ID:", info["video_id"])
    print("Title:", info["title"])
    print("Published At:", convert_time(info["published_at"]))
    print("View Count:", info["view_count"])
else:
    print("Không tìm thấy channel!")
