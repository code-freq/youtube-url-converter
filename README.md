# YouTube URL Converter

This project is a YouTube URL converter that allows users to download and convert YouTube videos to various formats, with the option to download audio, video, or both separately. Users can customize the quality and format for each, and the tool also provides an option to merge audio and video.

## Features
- **Download Options:** Choose to download either audio, video, or both from YouTube videos.
- **Format and Quality Selection:** Customize the output format and quality for both audio and video.
- **Merging Capability:** Merge selected audio and video files into a single output if it is needed.
- **Flexible Output:** Supports downloading files in different combinations, allowing users to select specific formats and qualities for audio and video separately.
- **Lightweight and Easy to Use:** Simple, user-friendly interface for quick and efficient conversions.
- **Powerful Tools:** Uses `yt-dlp` for downloading and `FFmpeg` for both audio and video processing. 
  
### Supported Formats
- MP3, MP4, AVI, WAV, M4A, FLAC, OGG, MKV, MOV, WEBM, FLV and MPEG.

## Requirements
- Python 3.x
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/download.html) (required for extracting audio)
- subprocess (Built-in)

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/code-freq/youtube-url-converter.git
```
### 2. Install the required packages:
```bash
pip install yt-dlp
```
### 3. Install ffmpeg
Follow the instructions [here](https://ffmpeg.org/download.html) to install ffmpeg on your system.

**_Ensure that `ffmpeg` is available in your system's PATH so that it can be used by `yt-dlp` during conversion._**

## Usage
1. Run `main.py`
2. Enter the YouTube URL.
3. Select the audio quality (or type none to skip audio download).
4. If you chose an audio quality, select the desired audio format.
5. Select the video quality (or type none to skip video download).
6. If you chose a video quality, select the desired video format.
7. If both audio and video are selected, choose whether to merge them into a single file.
8. Merged file will be downloaded to the current directory, with the file name formatted as <title> (merged).<ext>.

## How It Works
1. **YouTube Video Downloading:** The script utilizes `yt-dlp` to download the specified YouTube video based on the provided URL, ensuring that users have access to the latest video formats and quality options.
2. **Format and Quality Selection:** Users can customize their downloads by selecting the desired formats and quality for both audio and video through the options provided by `yt-dlp`, allowing for tailored outputs based on user preferences.
3. **Audio and Video Processing:** The script processes audio and video separately using `FFmpeg`, preparing each for conversion based on the selected formats.
4. **Merging:** `FFmpeg` is employed to merge the two files into a single output when required, ensuring high-quality results.

> [!IMPORTANT]
> If `ffmpeg` is not installed or not properly added to the PATH, the audio extraction will not work.

> [!TIP]
> **Use VLC for Playback:** It is recommended to use VLC Media Player for the best compatibility and playback of the downloaded audio and video files. VLC supports a wide range of formats and ensures smooth playback without issues.
> **Handling Temporary Server Errors:** Due to occasional discrepancies with YouTube's servers, audio and video quality options may differ. If this occurs, restarting the program a few times may help resolve the issue and improve the quality of the downloads.
> **Experiment with Different Formats:** When merging files, certain format selections may lead to security errors or application crashes. It is advisable to try different formats if you encounter any issues during the merging process to find the best combination that works for your needs.

## Contact

For suggestions, recommendations, development ideas, or any issues, feel free to reach out at [here](code.freq7@gmail.com).