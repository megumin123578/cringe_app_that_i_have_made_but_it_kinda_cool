import requests

webhook_url = "http://localhost:5678/webhook-test/from-python"

video_path = "sample.mp4"  # Đường dẫn file video

with open(video_path, "rb") as video_file:
    files = {
        "video": ("sample.mp4", video_file, "video/mp4")

    }
    data = {
        "title": "My Video",
        "description": "This is a test video"
    }

    response = requests.post(webhook_url, data=data, files=files)

    print("Gửi thành công:", response.status_code)
    print("Phản hồi:", response.text)
