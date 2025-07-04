import ffmpeg
import math

input_file = 'sample.mp4'
cropped_file = 'cropped.mp4'
output_file = 'out.mp4'


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

# get metadata tu video
probe = ffmpeg.probe(input_file)
video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')


original_width = int(video_stream['width'])
original_height = int(video_stream['height'])


crop_x = 100
crop_y = 50
crop_width = int(original_width - (original_width/100) * 40) 
crop_height = original_height


top_border, bottom_border = int((original_height/100) * 20), int((original_height/100) * 20) 

padded_height = crop_height + top_border + bottom_border

ffmpeg.input(input_file).output(
    cropped_file,
    vf=f'crop={crop_width}:{crop_height}:{crop_x}:{crop_y}',
    vcodec='libx264',
    acodec='aac'
).overwrite_output().run()


ffmpeg.input(cropped_file).output(
    output_file,
    vf=f'pad={crop_width}:{padded_height}:0:{top_border}:color=black',
    vcodec='libx264',
    acodec='aac'
).overwrite_output().run()

print(f'kich thuoc video goc: {original_width} x {original_height}')
print(f'kich thuoc video sau crop: {crop_width} x {crop_height}')
result = aspect_ratio(crop_width, crop_height)
print(f"Aspect Ratio: {result['ratio_simplified']}")
