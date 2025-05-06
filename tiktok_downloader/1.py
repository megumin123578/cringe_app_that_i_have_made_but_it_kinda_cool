import yt_dlp

def download_tiktok(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

url = input("Enter the TikTok video URL: ")
download_tiktok(url)