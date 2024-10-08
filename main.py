import yt_dlp

def fetch_audio(url, opts):
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    print("Download complete")

# list available audio formats, print them and get user selection
def format_selection(url) -> (str, str):
    available_formats = []
    with yt_dlp.YoutubeDL({"format":"all"}) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        duration = info_dict["duration"]
        mins = duration // 60
        secs = duration % 60
        duration = f"Duration: {mins} m, {secs} s"

        formats = info_dict.get("formats", [])

        print("\nAvailable formats:"
              "########################################################################")
        for f in formats:
            resolution = f["resolution"]
            if resolution == "audio only" and "asr" in f.keys():
                available_formats.append(f)

                print(f"Format ID: {f["format_id"]}  Audio Sampling Rate: {f["asr"]}  File Size: {round(f["filesize"]/1024, 2)} KB"
                      f"\nQuality: {f["quality"]}  Total Bit Rate: {f["tbr"]}  Codec: {f["acodec"]}  Extension: {f["audio_ext"]}")
                print("------------------------------------------------------------------------")

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

    return user_f_select, duration

url_input = input("Enter the video url: ").strip(" ")

format_choice, duration_str = format_selection(url_input)
print(duration_str)

# Audio file formats list that FFmpeg supports
output_formats = ["mp3", "aac", "m4a", "opus", "vorbis", "flac", "alac", "wav"]

# user input error handling loop
while True:
    codec_choice = input("Which audio file format do you want to convert to (e.g., mp3, m4a, wav): ")
    if not codec_choice in output_formats:
        print("Invalid output format")
        continue
    break

# create options
ydl_opts = {
        'format': str(format_choice),  # Download the desired format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': str(codec_choice),  # Convert to desired output format
        }],
        'outtmpl': '%(title)s.%(ext)s',  # Save with the video title
    }

fetch_audio(url_input, ydl_opts)
#https://www.youtube.com/watch?v=JcoKMe0XyqY