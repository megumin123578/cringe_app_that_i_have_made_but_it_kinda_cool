from moviepy import VideoFileClip, ColorClip, CompositeVideoClip

def process_video_to_vertical(input_file, output_file, crop_width=100, border_height=100):

    try:
        # Load the video
        video = VideoFileClip(input_file)

        # Get original dimensions
        orig_w, orig_h = video.size

        # Ensure crop_width doesn't exceed video width
        if crop_width >= orig_w:
            raise ValueError(f"Crop width ({crop_width}) cannot exceed video width ({orig_w})")

        # Crop the video (remove crop_width/2 from left and right)
        crop_x = crop_width // 2  # Pixels to crop from each side
        cropped_video = video.crop(x1=crop_x, x2=orig_w - crop_x)

        # Calculate new dimensions
        new_w = orig_w - crop_width
        new_h = orig_h + border_height  # Add borders to height

        # Create a black background clip for padding
        background = ColorClip(size=(new_w, new_h), color=(0, 0, 0), duration=video.duration)

        # Center the cropped video on the background (adds borders of border_height/2 on top/bottom)
        final_video = CompositeVideoClip(
            [background, cropped_video.set_position(("center", border_height // 2))]
        )

        # Write the output video
        final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")
        print(f"Video processed successfully! Output saved as {output_file}")

        # Close clips to free memory
        video.close()
        cropped_video.close()
        background.close()
        final_video.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "sample.mp4"
    output_file = "output.mp4"
    process_video_to_vertical(input_file, output_file, crop_width=100, border_height=100)