import yt_dlp

def youtube_to_mp3(video_url, save_path="./"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("Downloading and converting to MP3...")
        ydl.download([video_url])
        print("Conversion completed!")

# Example usage
video_url = input("Enter the YouTube video URL: ")
youtube_to_mp3(video_url)
