import subprocess

def process_video_to_vertical(input_file, output_file, crop_width=100, border_height=100, rotate=False):

    try:
        # Construct the FFmpeg filter
        if rotate:
            # Rotate 90 degrees, then crop and pad
            filter_complex = (f"rotate=90*PI/180,crop=in_h-{crop_width}:in_w,"
                              f"pad=in_w:in_h+{border_height}:0:{border_height//2}:black")
        else:
            # Crop to a vertical aspect ratio (e.g., 9:16) and pad
            filter_complex = (f"crop=in_w-{crop_width}:in_h,"
                              f"pad=in_w:in_h+{border_height}:0:{border_height//2}:black")

        # Construct the FFmpeg command
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', filter_complex,
            '-c:a', 'copy',  # Copy audio without re-encoding
            '-y',  # Overwrite output file if it exists
            output_file
        ]

        # Run the FFmpeg command
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Video processed successfully! Output saved as {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while processing video: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Ensure FFmpeg is installed and added to the system PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_video = "sample.mp4"
    output_video = "output.mp4"
    process_video_to_vertical(input_video, output_video, crop_width=100, border_height=100, rotate=False)