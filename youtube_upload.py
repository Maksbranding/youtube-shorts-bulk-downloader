from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import datetime

# Scopes for YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate():
    """
    Authenticate using OAuth 2.0 and return the authorized YouTube API client.
    Includes fallback to manual authorization in case of redirect_uri issues.
    """
    creds = None
    # Path to save the credentials token
    token_path = "token.pickle"
    try:
        # Check if token.pickle exists to reuse credentials
        if os.path.exists(token_path):
            print(f"Loading credentials from {token_path}...")
            with open(token_path, "rb") as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate the user
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                print("Starting new authentication flow...")
                flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
                try:
                    # Preferred method: Local server authentication
                    creds = flow.run_local_server(port=8080)
                except Exception:
                    # Fallback method: Manual authorization
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    print("Please visit this URL to authorize the application:")
                    print(auth_url)
                    code = input("Enter the authorization code here: ")
                    creds = flow.fetch_token(code=code)
            # Save the credentials for future use
            print(f"Saving credentials to {token_path}...")
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)
    except Exception as e:
        print(f"Error during authentication: {e}")
        raise e

    return build("youtube", "v3", credentials=creds)

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

def upload_video(youtube, file_path, title, schedule_time):
    """
    Upload and schedule a video to YouTube.
    """
    tags = generate_tags(title)
    description = generate_description(title)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22"  # Default category ID for 'People & Blogs'
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
    except Exception as e:
        print(f"Failed to upload video {title}. Error: {e}")

# Authenticate with OAuth
youtube = authenticate()

# Folder containing your videos
folder_path = "processed_videos"
valid_extensions = (".mp4", ".mov", ".avi", ".mkv")
videos = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)])

# Debug: Print filtered videos
print("Filtered videos:", videos)

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
    title = os.path.splitext(video_file)[0]
    schedule_time = start_date + datetime.timedelta(hours=i * upload_interval)
    upload_video(youtube, file_path, title, schedule_time)
    uploads_today += 1
