import subprocess

def process_video(input_file, output_file, crop_width=100, border_height=100):

    try:
   
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f'crop=in_w-{crop_width}:in_h,pad=in_w:in_h+{border_height}:0:{border_height//2}:black',
            '-y',  # Overwrite output file if it exists
            output_file
        ]
        
  
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Video processed successfully! Output saved as {output_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while processing video: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Ensure FFmpeg is installed and added to the system PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    input_video = "sample.mp4"
    output_video = "output.mp4"
    process_video(input_video, output_video, crop_width=100, border_height=100)