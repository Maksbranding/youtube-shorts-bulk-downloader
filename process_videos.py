from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from moviepy.video.fx import all as vfx
import os

INPUT_FOLDER = "downloaded_videos"
OUTPUT_FOLDER = "processed_videos"
LOGO_PATH = "logo.png"

def add_logo(video, logo_path):
    # Load the logo, increase size, and position it at the center top
    logo = (
        ImageClip(logo_path)
        .set_duration(video.duration)
        .resize(height=200)  # Increase logo size (4 times more than before)
        .set_position(("center", "top"))  # Position at center top
    )
    return CompositeVideoClip([video, logo])

def process_video(input_path, output_path, logo_path):
    # Load video and apply brightness and logo
    video = VideoFileClip(input_path)
    video = video.fx(vfx.colorx, 1.4)  # Increase brightness further (1.4x)
    video = add_logo(video, logo_path)
    
    # Export processed video
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video.close()

def process_videos(input_folder, logo_path):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for video_file in os.listdir(input_folder):
        if video_file.endswith((".mp4", ".avi", ".mov", ".mkv")): 
            input_path = os.path.join(input_folder, video_file)
            output_path = os.path.join(OUTPUT_FOLDER, video_file)
            print(f"Processing {video_file}...")
            process_video(input_path, output_path, logo_path)
            print(f"{video_file} processed and saved to {OUTPUT_FOLDER}.")

if __name__ == "__main__":
    process_videos(INPUT_FOLDER, LOGO_PATH)
