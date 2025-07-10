import os
import subprocess
import json
from moviepy import VideoFileClip

def get_video_duration(file_path):
    try:
        with VideoFileClip(file_path) as video:
            minute = int(round(video.duration)) // 60
            sec = int(round(video.duration)) % 60
            if sec < 10:
                sec = f'0{sec}'
            return f'{minute}:{sec}'
    except Exception as e:
        print(f"Error getting duration for '{file_path}': {e}")
        return "0:00"
def find_first_vid(first_vd): # return path, duration
    base_folder = r'\\nashp\DATABUHP\Nam SEO\.Bé Cá'
    main_folder = os.path.join(base_folder, f"{first_vd} BC")
    target_name = f"video edit {first_vd} bc"

    found_path = None
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.flv']

    try:
        for name in os.listdir(main_folder):
            full_path = os.path.join(main_folder, name)
            if os.path.isdir(full_path) and name.lower() == target_name:
                found_path = full_path
                break

        if found_path:       
            video_files = []
            for file in os.listdir(found_path):
                full_file_path = os.path.join(found_path, file)
                if os.path.isfile(full_file_path):
                    if any(file.lower().endswith(ext) for ext in video_extensions):
                        video_files.append(full_file_path)

            if video_files:
                first_video = video_files[0]
                duration = get_video_duration(first_video)
                return first_video, duration
            else:
                print("\nKhông tìm thấy video nào trong thư mục.")
        else:
            print("Không tìm thấy thư mục con:", os.path.join(main_folder, f"Video Edit {first_vd} BC"))
        return None, 0
    except Exception as e:
        print("Lỗi:", e)
        return None, 0
    


def normalize_video(input_path, output_path):
    command = [
        "ffmpeg", "-y",
        "-fflags", "+genpts",      # Sửa timestamp lỗi
        "-i", input_path,
        "-vf", "scale=1280:720",  
        "-r", "60",                # Chuẩn hóa FPS
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        "-movflags", "+faststart",
        output_path
    ]
    subprocess.run(command, check=True)



def concat_video(video_paths, output_path):
    list_file = "temp.txt"
    with open(list_file, 'w', encoding='utf-8') as f:
        for path in video_paths:
            abs_path = os.path.abspath(path).replace("\\", "/")
            f.write(f"file '{abs_path}'\n")

    command = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output_path
    ]
    subprocess.run(command, check=True)
    os.remove(list_file)

def auto_concat(input_videos, output_path):
    # Bước 1: Normalize tất cả video đầu vào
    normalized_paths = []
    for i, path in enumerate(input_videos):
        fixed = f"normalized_{i}.mp4"
        normalize_video(path, fixed)
        normalized_paths.append(fixed)

    concat_video(normalized_paths, output_path)
    
    for path in normalized_paths:
        os.remove(path)

    print("Ghép video hoàn tất:", output_path)

# debug
def print_video_info(video_path):
    print(f"\n🔍 Đang kiểm tra: {video_path}")

    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", video_path],
            capture_output=True, text=True, check=True
        )
        info = json.loads(result.stdout)

        for stream in info.get("streams", []):
            if stream.get("codec_type") == "video":
                print(f"VIDEO:")
                print(f"  Codec: {stream.get('codec_name')}")
                print(f"  Resolution: {stream.get('width')}x{stream.get('height')}")
                print(f"  FPS: {eval(stream.get('r_frame_rate')):.2f}")
                print(f"  Pixel format: {stream.get('pix_fmt')}")
            elif stream.get("codec_type") == "audio":
                print(f"AUDIO:")
                print(f"  Codec: {stream.get('codec_name')}")
                print(f"  Sample rate: {stream.get('sample_rate')} Hz")
                print(f"  Channels: {stream.get('channels')}")
        
        format_info = info.get("format", {})
        duration = float(format_info.get("duration", 0))
        print(f"Duration: {duration:.2f} seconds")

    except Exception as e:
        print(f"Lỗi khi đọc thông tin video: {e}")


