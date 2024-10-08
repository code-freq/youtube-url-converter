import yt_dlp

def fetch_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best audio format available
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',  # Convert to MP3
            'preferredquality': '192',  # Set desired audio quality
        }],
        'outtmpl': '%(title)s.%(ext)s',  # Save with the video title
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download complete")

url_input = input("Enter the video url: ").strip(" ")
fetch_audio(url_input)
