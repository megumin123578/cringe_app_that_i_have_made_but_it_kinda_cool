import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename


Tk().withdraw()
video_path = askopenfilename(
    title="Chọn file video để gửi lên n8n",
    filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
)

if not video_path:
    print("Bạn chưa chọn file nào.")
    exit()


webhook_url = "http://localhost:5678/webhook-test/http://localhost:5678/webhook/from-python"

with open(video_path, "rb") as video_file:
    files = {
        "video": (video_path.split("/")[-1], video_file, "video/mp4")
    }
    data = {
        "title": "Tự động gửi video",
        "description": "Gửi từ Python + tkinter"
    }

    response = requests.post(webhook_url, data=data, files=files)

    print("Gửi thành công:", response.status_code)
    print("Phản hồi:", response.text)
