import schedule
import time
import subprocess

def update_data():
    print("Cập nhật dữ liệu mới từ API YouTube...")
    subprocess.run(["python", "fetch_youtube_data.py"]) 


schedule.every(12).hours.do(update_data)

while True:
    schedule.run_pending()
    time.sleep(60)
