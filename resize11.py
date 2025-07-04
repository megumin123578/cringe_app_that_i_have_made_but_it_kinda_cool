import os
import ffmpeg

input_file = 'sample.mp4'  
output_file = 'output_2.mp4'  


if not os.path.exists(input_file):
    raise FileNotFoundError(f"Không tìm thấy file: {input_file}")

probe = ffmpeg.probe(input_file)
video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
original_width = int(video_stream['width'])
original_height = int(video_stream['height'])

print(f'📏 Kích thước video gốc: {original_width} x {original_height}')


filter_str = (
    'scale=-1:1350,'  
    'crop=1080:1350:(in_w-1080)/2:(in_h-1350)/2'
)


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


probe_out = ffmpeg.probe(output_file)
out_stream = next(stream for stream in probe_out['streams'] if stream['codec_type'] == 'video')
out_width = int(out_stream['width'])
out_height = int(out_stream['height'])

print(f"Video gốc: {original_width} x {original_height}")
print(f"Video sau xử lý: {out_width} x {out_height}")
