import yt_dlp
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor

def get_short_links(channel_url):
    """Extract all Shorts video links from a YouTube channel."""
    ydl_opts = {
        'quiet': False,  # Enable output for debugging
        'extract_flat': True,  # Extract metadata without downloading
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"{channel_url}/shorts", download=False)
            if 'entries' in result:
                short_links = [
                    f'https://www.youtube.com/shorts/{entry["id"]}'
                    for entry in result['entries']
                    if 'shorts' in entry.get('url', '')
                ]
                print(f"Extracted {len(short_links)} Shorts links.")
                return short_links
            else:
                print("No Shorts videos found.")
                return []
    except Exception as e:
        print(f"Error fetching Shorts links: {e}")
        return []

def download_video(link, output_path, cookies_path):
    """Download a single video."""
    try:
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'best',
            'noplaylist': True,
            'quiet': False,
            'ignoreerrors': True,
            'cookiefile': cookies_path,  # Load cookies from the file
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'headers': {
                'Accept-Language': 'en-US,en;q=0.9',
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print(f"Downloaded: {link}")
    except Exception as e:
        print(f"Error downloading {link}: {e}")

def download_videos_with_workers(links, output_path, cookies_path, max_workers=20):
    """Download videos concurrently using multiple workers."""
    print(f"Using cookies from: {cookies_path}")
    os.makedirs(output_path, exist_ok=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for link in links:
            executor.submit(download_video, link, output_path, cookies_path)
            # Add random delay between each task submission
            time.sleep(random.randint(3, 15))

def main():
    """Main function for command-line execution."""
    # Hardcoded channel URL
    channel_url = "https://www.youtube.com/@RCDriftTok"

    # Path to cookies.txt
    cookies_path = "cookies.txt"  # Ensure this file exists

    # Default output directory
    output_path = "downloaded_videos"

    # Extract Shorts video links
    print(f"Fetching Shorts video links from {channel_url}...")
    short_links = get_short_links(channel_url)
    if not short_links:
        print("No Shorts videos found.")
        return

    # Skip already downloaded videos (adjust as needed)
    already_downloaded_count = 350
    short_links = short_links[already_downloaded_count:]

    # Download videos using workers
    print(f"Found {len(short_links)} Shorts videos. Starting download...")
    download_videos_with_workers(short_links, output_path, cookies_path, max_workers=20)
    print(f"Download process completed! Videos saved in: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()
