# youtube_playlist_download

A YouTube web scraping script that allows for the downloading and extraction of metadata (Title, Artist) from a given YouTube music playlist.

## Installation

```
git clone https://github.com/jasonshin1127/youtube_playlist_download.git
python3 -m venv myenv
source myenv/bin/activate
pip install pytube yt-dlp ytmusicapi selenium beautifulsoup4 lxml
```

## Command

```
python music_download.py 'YOUR_PLAYLIST_URL'
```

## Output

The soundtrack of the video will be downloaded in MP3 format under the /musics directory.

The metadata of the soundtrack, including the music name, artist, and relative path of the MP3 file, will be saved in the music_metadata.json file in the following format:

(Example Metadata Format)

<img width="737" alt="image" src="https://github.com/user-attachments/assets/bc02e1cb-85b9-4c6b-8ad5-4f17acc52a5a">
