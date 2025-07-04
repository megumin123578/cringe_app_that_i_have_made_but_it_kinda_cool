from moviepy import VideoFileClip

input_file = 'sample.mp4'
width = 1080
height = 900

video = VideoFileClip(input_file)
resized_vid = video.resized((width,height))
ouput_file = 'out_put.mp4'
resized_vid.write_videofile(ouput_file)