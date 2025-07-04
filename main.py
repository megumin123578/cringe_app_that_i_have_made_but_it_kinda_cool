import ffmpeg
import math

input_file = 'sample2.mp4'
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
origin_ratio = aspect_ratio(original_width, original_height)
result = aspect_ratio(crop_width, crop_height)
print(f"Aspect Ratio video goc: {origin_ratio['ratio_simplified']}")
print(f"Aspect Ratio sau crop: {result['ratio_simplified']}")
