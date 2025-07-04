
import os
import subprocess
import json




def concat_video(video_paths, output_path, re_encode=False):
    try:
        for path in video_paths:
            if not os.path.exists(path):
                print(f"Không có video tại đường dẫn {path}")
                return False

        temp_file = 'temp.txt'
        with open(temp_file, 'w', encoding='utf-8') as f:
            for path in video_paths:
                abs_path = os.path.abspath(path).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")

        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", temp_file
        ]

        if re_encode:
            command += [
                "-c:v", "libx264",        
                "-preset", "fast",        
                "-c:a", "aac",             
                "-movflags", "+faststart", 
                output_path
            ]
        else:
            command += [
                "-c", "copy",
                output_path
            ]

        # result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Video được lưu tại: {output_path}")

        os.remove(temp_file)
        return True

    except subprocess.CalledProcessError as e:
        print("Lỗi ffmpeg:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    

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

if __name__ == '__main__':
    video_files = [
        '1.mp4',
        '2.mp4',
        '3.mp4'
        
    ]
    output_path = 'output.mp4'
    for video in video_files:
        print_video_info(video)

    concat_video(video_files, output_path, re_encode=False)
