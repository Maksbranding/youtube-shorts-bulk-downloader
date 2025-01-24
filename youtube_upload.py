from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import datetime

# Your YouTube API key
API_KEY = "AIzaSyAcPcPnqXM1yJ3aCX-hk3ZW7g0Y2b7s8Yw"

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def generate_tags(title):
    """
    Generate tags based on the title.
    """
    tags = title.split()
    tags.extend(["Shorts", "YouTube", "Trending"])
    return tags

def generate_description(title):
    """
    Generate a description based on the title.
    """
    description = f"This video is titled '{title}'. Enjoy watching this amazing content! Don't forget to like and subscribe."
    return description

def upload_video(file_path, title, schedule_time):
    """
    Upload and schedule a video to YouTube.
    """
    tags = generate_tags(title)  # Generate tags
    description = generate_description(title)  # Generate description

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": schedule_time.isoformat() + "Z"
            }
        },
        media_body=MediaFileUpload(file_path)
    )
    response = request.execute()
    print(f"Uploaded: {title} | Scheduled for: {schedule_time}")
    return response

# Folder containing your videos
folder_path = "Processed_videos"
videos = sorted(os.listdir(folder_path))

# Limit uploads to 6 videos per day
MAX_DAILY_UPLOADS = 6
uploads_today = 0

# Start scheduling from now
start_date = datetime.datetime.now()
upload_interval = 8  # 8 hours between uploads (3 per day)

for i, video_file in enumerate(videos):
    if uploads_today >= MAX_DAILY_UPLOADS:
        print("Reached daily quota. Please run the script again tomorrow.")
        break

    file_path = os.path.join(folder_path, video_file)
    title = os.path.splitext(video_file)[0]  # Use file name as title
    schedule_time = start_date + datetime.timedelta(hours=i * upload_interval)
    upload_video(file_path, title, schedule_time)
    uploads_today += 1
