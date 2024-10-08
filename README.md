# YouTube URL to MP3 Converter

This project is a simple YouTube URL to MP3 converter. It takes a YouTube video URL as input and converts the audio track of the video into an MP3 file.

## Features
- Convert YouTube videos to MP3 format.
- Audio quality selection. 
- Output format selection.
- Lightweight and easy to use.
- Uses `yt-dlp` for downloading and `ffmpeg` for audio extraction.
  
## Requirements
- Python 3.x
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/download.html) (required for extracting audio)

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/code-freq/youtube-url-to-mp3-converter.git
```
### 2. Install the required packages:
```bash
pip install yt-dlp
```
### 3. Install ffmpeg
Follow the instructions [here](https://ffmpeg.org/download.html) to install ffmpeg on your system.

**_Ensure that `ffmpeg` is available in your system's PATH so that it can be used by `yt-dlp` during conversion._**

## Usage
Run `main.py` and enter the Youtube URL.
The script will download the video and extract the audio into MP3 format, saving it in the current directory.

## How It Works
- The script uses `yt-dlp` to download the YouTube video.
- Audio is extracted from the video in MP3 format using `ffmpeg`.
- Output MP3 files are saved to the current directory with the video title as the filename.

> [!IMPORTANT]
> If `ffmpeg` is not installed or not properly added to the PATH, the audio extraction will not work.
