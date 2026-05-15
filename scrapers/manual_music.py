import os
import random
from youtube_search import YoutubeSearch
import yt_dlp

def search_anime_osts(anime_name, max_results=4):
    """Search for anime OSTs on YouTube."""
    search_query = f"{anime_name} full ost -extended"
    results = YoutubeSearch(search_query, max_results=max_results).to_dict()
    video_list = []
    for video in results:
        title = video['title']
        url = f"https://www.youtube.com{video['url_suffix']}"
        video_list.append((title, url))
    return video_list

def sanitize_title(title):
    """Sanitize the video title to make it file-system safe."""
    return "".join(c if c.isalnum() else "_" for c in title)

def download_clips(url, duration, title, sanitized_title, output_path="music-clips", num_clips=2, clip_duration=10):
    """Download clips from a YouTube video using yt-dlp."""
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(f"Processing video: {title}")
    for i in range(num_clips):
        start_time = random.uniform(0, max(0, duration - clip_duration))
        end_time = start_time + clip_duration
        output_file = os.path.join(output_path, f"{sanitized_title}_clip_{i + 1}.mp3")
        yt_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_file,
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
            ],
            "download_ranges": lambda info_dict, yt_instance: [
    			{'start_time': start_time, 'end_time': end_time, 'title': 'first_section'},
    		],
            "force_keyframes_at_cuts": True,
        }
        with yt_dlp.YoutubeDL(yt_opts) as clip_ydl:
            clip_ydl.download([url])

if __name__ == "__main__":
    anime_name = input("Enter the anime name: ").strip()
    osts = search_anime_osts(anime_name)

    if not osts:
        print("\nNo results found.")
        exit()

    long_video = None
    other_videos = []

    print("\nAnalyzing search results...")
    for title, url in osts:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            duration = info.get("duration", 0)
            sanitized_title = sanitize_title(info.get("title", "Unknown Title"))
            if duration > 15 * 60:
                long_video = (title, url, duration, sanitized_title)
                break  # Prioritize long video and stop checking others
            other_videos.append((title, url, duration, sanitized_title))

    output_path=f"music-clips/{anime_name}"
    if long_video:
        # Use the long video
        print(f"\nFound a long video: {long_video[0]} ({long_video[2]} seconds)")
        download_clips(long_video[1], long_video[2], long_video[0], long_video[3], output_path=output_path, num_clips=4)
    else:
        # Use up to 4 shorter videos
        print("\nNo long video found. Using multiple shorter videos.")
        for video in other_videos[:4]:
            title, url, duration, sanitized_title = video
            download_clips(url, duration, title, sanitized_title, output_path=output_path)
