
import math
import os
import datetime
import ffmpeg
import subprocess
import json

################################ FUNCTION ######################################

def concat_video(video_paths, re_encode=False):
    temp_name = datetime.datetime.now()
    output_file = f'{get_name(temp_name)}.mp4'
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
                output_file
            ]
        else:
            command += [
                "-c", "copy",
                output_file
            ]

        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Video lưu lại với tên: {output_file}")

        os.remove(temp_file)
        return output_file

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


def get_name(name):
    for i, char in enumerate(str(name)):
        if char == '.':
            name = str(name)[:i].replace(':','_').replace('-','_')
            return name

def simplify_ratio(width, height):
    gcd = math.gcd(width, height)
    return width // gcd, height // gcd

def aspect_ratio(width, height):
    ratio = width / height
    simplified = simplify_ratio(width, height)
    return {
        "width": width,
        "height": height,
        "ratio_decimal": round(ratio, 4),
        "ratio_simplified": f"{simplified[0]}:{simplified[1]}"
    }

def resize_video(input_file):

    temp_name = datetime.datetime.now()

    temp_file = 'temp.mp4'
    output_file = f'{get_name(temp_name)}.mp4'

    probe = ffmpeg.probe(input_file)
    video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')


    original_width = int(video_stream['width'])
    original_height = int(video_stream['height'])

    target_ratio = 4 / 5
    target_width = int(original_height * target_ratio)


    if target_width <= original_width:
        crop_width = target_width
        crop_height = original_height
        crop_x = (original_width - crop_width) // 2
        crop_y = 0
    else:

        crop_width = original_width
        crop_height = int(original_width / target_ratio)
        crop_x = 0
        crop_y = (original_height - crop_height) // 2


    top_border, bottom_border = int((original_height/100) * 20), int((original_height/100) * 20) 

    padded_height = crop_height + top_border + bottom_border

    ffmpeg.input(input_file).output(
        temp_file,
        vf=f'crop={crop_width}:{crop_height}:{crop_x}:{crop_y}',
        vcodec='libx264',
        acodec='aac'
    ).overwrite_output().run()


    ffmpeg.input(temp_file).output(
        output_file,
        vf=f'pad={crop_width}:{padded_height}:0:{top_border}:color=black',
        vcodec='libx264',
        acodec='aac'
    ).overwrite_output().run()

    #delete cropped temp file
    os.remove(temp_file)
    print(f'kich thuoc video goc: {original_width} x {original_height}')
    print(f'kich thuoc video sau crop: {crop_width} x {crop_height}')
    origin_ratio = aspect_ratio(original_width, original_height)
    result = aspect_ratio(crop_width, crop_height)
    print(f"Aspect Ratio video goc: {origin_ratio['ratio_simplified']}")
    print(f"Aspect Ratio sau crop: {result['ratio_simplified']}")


#######################################################################