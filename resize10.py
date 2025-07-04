import os
import ffmpeg

input_file = 'sample.mp4'
output_file = 'tiktok_ready.mp4'

if not os.path.exists(input_file):
    raise FileNotFoundError(f"Không tìm thấy file: {input_file}")

# Lấy thông tin gốc
probe = ffmpeg.probe(input_file)
video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
original_width = int(video_stream['width'])
original_height = int(video_stream['height'])

print(f'Kích thước video đầu vào: {original_width} x {original_height}')

# Step 1: scale chiều cao về 1920, giữ nguyên tỉ lệ
# w=-1 để FFmpeg tự tính chiều rộng tương ứng
# Sau đó ta sẽ crop ngang và pad nếu cần

# Step 2: Giữ 60% chiều ngang
filter_str = (
    'scale=-1:1920,'  # scale chiều cao = 1920
    'crop=ih*9/16:ih:(iw-(ih*9/16))/2:0,'  # crop theo tỉ lệ 9:16 từ chiều rộng
    'pad=1080:1920:(1080-iw)/2:(1920-ih)/2:black'  # pad ngang nếu cần
)

print("Filter đang dùng:", filter_str)

# Thực thi ffmpeg
try:
    ffmpeg.input(input_file).output(
        output_file,
        vf=filter_str,
        vcodec='libx264',
        acodec='aac',
        preset='fast',
        movflags='faststart'
    ).overwrite_output().run()
except ffmpeg.Error as e:
    print("LỖI FFmpeg:")
    print(e.stderr.decode(errors='ignore'))
    raise

# Kiểm tra kích thước sau xử lý
probe_out = ffmpeg.probe(output_file)
video_out_stream = next(stream for stream in probe_out['streams'] if stream['codec_type'] == 'video')
out_width = int(video_out_stream['width'])
out_height = int(video_out_stream['height'])

print(f"Kích thước video sau xử lý: {out_width} x {out_height}")
