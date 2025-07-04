from moviepy import VideoFileClip, ColorClip, CompositeVideoClip
from moviepy import crop

def process_video_to_vertical(input_file, output_file, target_width=1080, target_height=900, border_height=100):

    try:
        # Load the video
        video = VideoFileClip(input_file)

        # Get original dimensions
        orig_w, orig_h = video.size

        # Calculate crop width to achieve target aspect ratio
        # Target aspect ratio = target_width / target_height
        target_aspect = target_width / target_height
        desired_width = int(orig_h * target_aspect)  # Width to match target aspect ratio
        crop_width = max(0, orig_w - desired_width)  # Total pixels to crop
        if crop_width >= orig_w:
            raise ValueError(f"Crop width ({crop_width}) cannot exceed video width ({orig_w})")

        # Crop the video (remove crop_width/2 from left and right)
        crop_x = crop_width // 2
        cropped_video = crop(video, x1=crop_x, x2=orig_w - crop_x)

        # Resize to target dimensions
        resized_video = cropped_video.resize((target_width, target_height))

        # Create a black background clip for padding
        final_height = target_height + border_height  # Add borders to height
        background = ColorClip(size=(target_width, final_height), color=(0, 0, 0), duration=video.duration)

        # Center the resized video on the background (adds borders of border_height/2 on top/bottom)
        final_video = CompositeVideoClip(
            [background, resized_video.set_position(("center", border_height // 2))]
        )

        # Write the output video
        final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
        print(f"Video processed successfully! Output saved as {output_file}")

        # Close clips to free memory
        video.close()
        cropped_video.close()
        resized_video.close()
        background.close()
        final_video.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "sample.mp4"
    output_file = "output.mp4"
    process_video_to_vertical(input_file, output_file, target_width=1080, target_height=900, border_height=100)