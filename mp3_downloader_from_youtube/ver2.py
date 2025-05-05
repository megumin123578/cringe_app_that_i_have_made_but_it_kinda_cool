import os
import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp

def download_mp3():
    video_url = url_entry.get()
    if not video_url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL.")
        return

    save_dir = filedialog.askdirectory(title="Choose folder to save MP3")
    if not save_dir:
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': 'C:/ffmpeg/ffmpeg-6.1-full_build/bin',  # <-- chỉnh đúng đường dẫn nếu cần
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            status_label.config(text="Downloading and converting...")
            ydl.download([video_url])
            status_label.config(text="Done! MP3 saved.")
            messagebox.showinfo("Success", "Download and conversion complete!")
    except Exception as e:
        status_label.config(text="Error occurred.")
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

# ----- GUI setup -----
root = tk.Tk()
root.title("YouTube to MP3 Downloader")
root.geometry("500x180")

tk.Label(root, text="Enter YouTube video URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

tk.Button(root, text="Download as MP3", command=download_mp3, bg="#4CAF50", fg="white").pack(pady=10)

status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

root.mainloop()
