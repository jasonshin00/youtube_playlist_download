import json
from pytube import Playlist
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import argparse

ytmusic = YTMusic()

parser = argparse.ArgumentParser(description="Download music from YouTube playlist and extract metadata.")
parser.add_argument('playlist_url', type=str, help="URL of the YouTube playlist to download.")
parser.add_argument('--download_directory', type=str, default='musics/', help="Directory to save downloaded music.")
args = parser.parse_args()

playlist_url = args.playlist_url
download_directory = args.download_directory
playlist = Playlist(playlist_url)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': os.path.join(download_directory, '%(title)s.%(ext)s'),
}

metadata_dict = {}
driver = webdriver.Chrome()

def extract_title_artist(url):
    driver.get('{}/videos?view=0&sort=p&flow=grid'.format(url))
    content = driver.page_source.encode('utf-8').strip()
    html_text = str(BeautifulSoup(content, 'lxml'))
    pattern = r'"imageStyle":"(.*?)","title":"(.*?)","subtitle":"(.*?)"'
    extracted_data = re.findall(pattern, html_text)
    return {"music_name": extracted_data[0][1], "artist": extracted_data[0][2]}

for video in playlist.videos:
    video_id = video.video_id
    video_info = ytmusic.get_song(video_id)
    try:
        title_artist_info = extract_title_artist(video.watch_url)
        music_name = title_artist_info.get("music_name", "Unknown Title")
        artist = title_artist_info.get("artist", "Unknown Artist")
    except Exception as e:
        print(f"Error processing video ID {video_id}: {e}")
        music_name = video_info['videoDetails']['title']
        artist = video_info['videoDetails']['author']

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video.watch_url])
    relative_path = os.path.relpath(os.path.join(download_directory, f"{music_name}.mp3"), os.getcwd())
    metadata = {
        'music_name': music_name,
        'artist': artist,
        'relative_path': relative_path
    }
    
    metadata_dict[video_id] = metadata
    with open('music_metadata.json', 'w') as f:
        json.dump(metadata_dict, f, indent=4)

print("Download and metadata extraction completed.")
