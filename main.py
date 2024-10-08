import yt_dlp

def fetch_audio(url, opts):
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    print("Download complete")

# list available audio formats, print them and get user selection
def format_selection(url) -> str:
    available_formats = []
    with yt_dlp.YoutubeDL({"format":"all"}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get("formats", [])

        print("Available formats:\n")
        for f in formats:
            resolution = f["resolution"]
            if resolution == "audio only" and "asr" in f.keys():
                available_formats.append(f)

                print(f"Format ID: {f["format_id"]}  Audio Sampling Rate: {f["asr"]}  File Size: {round(f["filesize"]/1024, 2)} KB"
                      f"\nQuality: {f["quality"]}  Total Bit Rate: {f["tbr"]}  Codec: {f["acodec"]}  Extension: {f["audio_ext"]}")
                print("--------------------------------------------------------------------------------------------------------")

        # gather ID's
        ids = []
        [ids.append(i["format_id"]) for i in available_formats]

        # user input error handling loop
        while True:
            user_f_select = input("Please select format ID: ")
            if user_f_select not in ids:
                print("Invalid format ID")
                continue
            break


    return user_f_select

url_input = input("Enter the video url: ").strip(" ")

format_choice = format_selection(url_input)

# create options
ydl_opts = {
        'format': str(format_choice),  # Download all formats available
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',  # Convert to MP3
            'preferredquality': '192',  # Set desired audio quality
        }],
        'outtmpl': '%(title)s.%(ext)s',  # Save with the video title
    }

fetch_audio(url_input, ydl_opts)
