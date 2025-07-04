import requests

data = {
    "username": "Megumin",
    "status": "done",
    "score": 100
}

webhook_url = "http://localhost:5678/webhook-test/http://localhost:5678/webhook/from-python"

try:
    response = requests.post(webhook_url, json=data)
    print("Gửi thành công:", response.status_code)
    print("Phản hồi:", response.text)
except Exception as e:
    print("Lỗi:", e)
