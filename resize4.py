import ffmpeg

input_file = 'sample.mp4'
output_file = 'out.mp4'

# Lấy metadata từ video
probe = ffmpeg.probe(input_file)

# Lọc luồng video (loại codec_type = 'video')
video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')

width = int(video_stream['width']) - 1000
height = int(video_stream['height'])

x = 100
y = 50

# FFmpeg crop
ffmpeg.input(input_file).output(
    output_file,
    vf=f'crop={width}:{height}:{x}:{y}',
    vcodec='libx264',
    acodec='aac'
).run()
