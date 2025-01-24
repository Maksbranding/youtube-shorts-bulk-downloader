import yt_dlp
import os
import time
import random


def get_short_links(channel_url):
    """Extract Shorts video links from a YouTube channel."""
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
                print(f"Extracted Shorts links: {short_links}")
                return short_links
            else:
                print("No Shorts videos found.")
                return []
    except Exception as e:
        print(f"Error fetching Shorts links: {e}")
        return []


def download_videos_from_links(links, output_path, cookies_path, start_index=0):
    """Download videos from the list of links with a delay to avoid bot detection."""
    total_links = len(links)

    # Start downloading from the given index
    print(f"Resuming download from video {start_index + 1}...")
    links = links[start_index:]

    print(f"Using cookies from: {cookies_path}")
    for index, link in enumerate(links, start=1):
        link = link.strip()
        try:
            ydl_opts = {
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'format': 'best',
                'noplaylist': True,
                'quiet': False,
                'ignoreerrors': True,
                'cookiefile': cookies_path,  # Load cookies from the file
                'user_agent': random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
                ]),
                'headers': {
                    'Accept-Language': 'en-US,en;q=0.9',
                },
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            print(f"Downloaded video {index}/{total_links}: {link}")
        except Exception as e:
            print(f"Error downloading {link}: {e}")
        finally:
            # Pause after every 30 videos to avoid detection
            if index % 30 == 0:
                print("Batch completed. Waiting for 60 minutes...")
                time.sleep(3600)  # Pause for 1 hour
            else:
                delay = random.randint(20, 40)  # Random delay between downloads
                print(f"Waiting for {delay} seconds before the next download...")
                time.sleep(delay)


def main():
    """Main function for command-line execution."""
    # Hardcoded channel URL
    channel_url = "https://www.youtube.com/@RCDriftTok"

    # Path to cookies.txt
    cookies_path = "cookies.txt"  # Ensure this file exists

    # Default output directory
    output_path = "downloaded_videos"

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Extract Shorts video links
    print(f"Fetching Shorts video links from {channel_url}...")
    short_links = get_short_links(channel_url)
    if not short_links:
        print("No Shorts videos found.")
        return

    # Specify the starting index (to skip already downloaded videos)
    start_index = 54  # Change this if the number of downloaded videos varies

    # Download the videos with a delay
    print(f"Found {len(short_links)} Shorts videos. Starting download from video {start_index + 1}...")
    download_videos_from_links(short_links, output_path, cookies_path, start_index=start_index)
    print(f"Download process completed! Videos saved in: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
