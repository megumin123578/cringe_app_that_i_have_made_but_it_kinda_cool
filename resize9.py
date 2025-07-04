import os
import ffmpeg

input_file = 'sample.mp4'
output_file = 'tiktok_ready.mp4'

if not os.path.exists(input_file):
    raise FileNotFoundError(f"Không tìm thấy file: {input_file}")

probe = ffmpeg.probe(input_file)
video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
original_width = int(video_stream['width'])
original_height = int(video_stream['height'])

target_width = original_width - int(original_width / 100 * 40)
target_height = original_height

filter_str = (
    f'scale=-1:{target_height},'
    f'crop={target_width}:{target_height}:(in_w-{target_width})/2:0'
)

ffmpeg.input(input_file).output(
    output_file,
    vf=filter_str,
    vcodec='libx264',
    acodec='aac',
    preset='fast',
    movflags='faststart'
).run()

probe_out = ffmpeg.probe(output_file)
video_out_stream = next(stream for stream in probe_out['streams'] if stream['codec_type'] == 'video')

out_width = int(video_out_stream['width'])
out_height = int(video_out_stream['height'])

print(f'Kích thước video đầu vào: {original_width} x {original_height}')
print(f"Kích thước video sau xử lý: {out_width} x {out_height}")
