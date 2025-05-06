import tkinter as tk
from tkinter import ttk, messagebox
import threading
import yt_dlp

def download_tiktok(url, status_label):
    def run():
        try:
            status_label.config(text="⏳ Đang tải...", foreground="blue")
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'mp4'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            status_label.config(text="✅ Tải xong!", foreground="green")
        except Exception as e:
            status_label.config(text="❌ Lỗi khi tải video", foreground="red")
            messagebox.showerror("Lỗi", str(e))

    threading.Thread(target=run).start()

def on_download_click():
    url = url_var.get().strip()
    if not url:
        messagebox.showwarning("Thiếu URL", "Vui lòng nhập liên kết TikTok.")
        return
    download_tiktok(url, status_label)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("TikTok Downloader")
root.geometry("500x200")
root.resizable(False, False)

font_style = ("Segoe UI", 12)

tk.Label(root, text="Nhập liên kết TikTok:", font=font_style).pack(pady=10)

url_var = tk.StringVar()
url_entry = ttk.Entry(root, textvariable=url_var, font=font_style, width=50)
url_entry.pack(pady=5)

download_btn = ttk.Button(root, text="Tải video", command=on_download_click)
download_btn.pack(pady=10)

status_label = tk.Label(root, text="", font=font_style)
status_label.pack()

root.mainloop()
