import yt_dlp
import subprocess


# FUNCTIONS --------------------------------------------------------------------------

# download the file at the stream url with the options given
def fetch(url, opts):
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    print("Download complete")

# get info dict of all formats
def get_info(url) -> dict:
    with yt_dlp.YoutubeDL({"format":"all"}) as ydl:
        inf_dict = ydl.extract_info(url, download=False)
    return inf_dict

# list available audio formats, print them and get user selection
def audio_format_selection(info_dict) -> (str, str, str):
    available_audio_formats = []

    duration = info_dict["duration"]
    hours = duration // 3600
    mins = duration // 60
    secs = duration % 60
    duration = f"Duration: {hours} h, {mins} m, {secs} s\n"

    formats = info_dict.get("formats", [])

    # list available audio formats
    print("\nAvailable audio formats:\n"
          "########################################################################")
    for f in formats:
        resolution = f["resolution"]
        if resolution == "audio only" and not f.get("asr") is None:
            available_audio_formats.append(f)

            print(f"Format ID: {f["format_id"]}  Audio Sampling Rate: {f["asr"]}  File Size: {round(f["filesize"]/1024, 2)} KB"
                  f"\nQuality: {f["quality"]}  Average Bit Rate: {f["abr"]}  Codec: {f["acodec"]}  Extension: {f["audio_ext"]}")
            print("------------------------------------------------------------------------")

    # gather audio format ID's
    audio_ids = []
    [audio_ids.append(i["format_id"]) for i in available_audio_formats]
    audio_ids.append("none")

    # user input error handling loop
    selected_codec = None
    while True:
        user_af_select = input("Please select audio format ID (Enter 'none' for no audio): ")
        if user_af_select not in audio_ids:
            print("Invalid format ID")
            continue
        # get codec of the selected format
        selected_codec = next((i["acodec"].split(".", 1)[0] for i in available_audio_formats if str(i["format_id"]) == user_af_select), None)
        break

    return user_af_select, selected_codec, duration

# list available video formats, print them and get user selection
def video_format_selection(info_dict) -> (str, str, str):
    available_video_formats = []

    duration = info_dict["duration"]
    hours = duration // 3600
    mins = duration // 60
    secs = duration % 60
    duration = f"Duration: {hours} h, {mins} m, {secs} s"

    formats = info_dict.get("formats", [])

    # list available video formats
    print("\nAvailable video formats:\n"
          "########################################################################")
    for f in formats:
        if "asr" in f.keys() and f["asr"] is None:  # get only video formats
            available_video_formats.append(f)

            print(
                f"Format ID: {f["format_id"]}  File Size: {round(f["filesize"] / (1024 * 1024), 2)} MB"
                f"\nQuality: {f["quality"]}  Average Video Bit Rate: {f["vbr"]}  Codec: {f["vcodec"]}  "
                f"Extension: {f["video_ext"]}  Resolution: {f["resolution"]} ({f["format_note"]})")
            print("------------------------------------------------------------------------")

    # gather video format ID's
    video_ids = []
    [video_ids.append(i["format_id"]) for i in available_video_formats]
    video_ids.append("none")

    # user input error handling loop
    selected_codec = None
    while True:
        user_vf_select = input("Please select video format ID (Enter 'none' for no video): ")
        if user_vf_select not in video_ids:
            print("Invalid format ID")
            continue
        # get codec of the selected format
        selected_codec = next((i["vcodec"].split(".",1)[0] for i in available_video_formats if str(i["format_id"]) == user_vf_select), None)
        break

    return user_vf_select, selected_codec, duration

# merge video and audio
def merge_video_audio(video_file, audio_file, output_file):
    command = [
        'ffmpeg', '-i', video_file, '-i', audio_file,
        '-c:v', 'copy', '-c:a', 'aac', output_file
    ]
    subprocess.run(command)

# MAIN ---------------------------------------------------------------------------------

url_input = input("Enter the video url: ").strip(" ")  # get URL
info_dict_ = get_info(url_input)  # get info dict
vcodec_choice = None

# AUDIO PART ---------------------------------------------------------------------------
af_choice, codec, duration_str = audio_format_selection(info_dict_)
print(duration_str)

if not af_choice == "none":
    user_query = None
    audio_output_formats = None

    # specify available output formats and get user input in order to selected codec
    if codec == "mp4a":
        user_query = (" codec --> format\n"
                      "   mp3 --> mp3\n"
                      "   wav --> wav\n"
                      "   m4a --> m4a\n"
                      "  none --> m4a\n"
                      "   aac --> m4a\n"
                      "  alac --> m4a\n"
                      "  flac --> flac\n"
                      "vorbis --> ogg")

        # Audio file formats list that mp4a codec is compatible with
        audio_output_formats = ["mp3", "wav", "m4a", "flac", "vorbis", "alac", "none"]

    elif codec == "opus":
        user_query = ("(codec --> format)\n"
                      "   wav --> wav\n"
                      "   mp3 --> mp3\n"
                      "   m4a --> m4a\n"
                      "   aac --> m4a\n"
                      "  none --> webm\n"
                      "  flac --> flac\n")

        # Audio file formats list that mp4a codec is compatible with
        audio_output_formats = ["wav", "flac", "aac", "m4a", "none", "mp3"]

    else:
        print("Unrecognized video file extension..")
        exit()

    # print user query text
    print(f"Which audio file format do you want to convert to?\n"
          f"In order to format you want, select output codec please.\n"
          f"{user_query}"
          f"('none' for no conversion)")

    # user input error handling loop
    while True:
        acodec_choice = input(":")
        if not acodec_choice in audio_output_formats:
            print("Invalid output format")
            continue
        break

    # create options
    if acodec_choice == "none":
        audio_ydl_opts = {
            'format': af_choice,  # Download the desired format
            'outtmpl': '%(title)s.%(ext)s',  # Save with the video title
        }
    else:
        audio_ydl_opts = {
                'format': af_choice,  # Download the desired format
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
                    'preferredcodec': acodec_choice,  # Convert to desired output format
                }],
                'outtmpl': '%(title)s.%(ext)s',  # Save with the video title
            }

    fetch(url_input, audio_ydl_opts)  # fetch and download

# VIDEO PART ----------------------------------------------------------------------------
vf_choice, codec, duration_str = video_format_selection(info_dict_)
print(duration_str)

if not vf_choice == "none":
    user_query = None
    video_output_formats = None

    # specify available output formats and get user input in order to selected extension
    if codec == "av01":
        user_query = "mp4, webm, ogg, mkv, avi, mov, flv, mpeg"

        # Video file formats list that 'av1' codec is compatible with
        video_output_formats = ["mp4", "webm", "ogg", "mkv", "avi", "mov", "flv", "mpeg"]

    elif codec == "avc1" or codec == "vp09":
        user_query = "mp4, webm, mkv, avi, mov, flv, mpeg"

        # Video file formats list that 'avc' and 'vp9' codecs are compatible with
        video_output_formats = ["mp4", "webm", "mkv", "avi", "mov", "flv", "mpeg"]

    elif codec == "vp08":  # for old youtube videos
        user_query = "webm"

        # Video file formats list that 'vp8' codec is compatible with
        video_output_formats = ["webm"]

    else:
        print("Unrecognized video file extension..")
        exit()

    print(f"Which video file format do you want to convert to ({user_query})")

    # user input error handling loop
    while True:
        vcodec_choice = input(":")
        if not vcodec_choice in video_output_formats:
            print("Invalid output format")
            continue
        break

    # create options
    video_ydl_opts = {
            'format': vf_choice,  # Download the desired format
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',  # Use FFmpeg to extract audio
                'preferedformat': vcodec_choice,  # Convert to desired output format
            }],
            'outtmpl': '%(title)s.%(ext)s',  # Save with the video title
        }


    fetch(url_input, video_ydl_opts)  # fetch and download

# MERGING PART --------------------------------------------------------------------------

# get user permission with error handle loop
if not vf_choice == "none" and not af_choice == "none":
    print("Do you want to merge these files? (y/n)")
    while True:
        user_perm = input(":")
        if user_perm.lower() == "y":
            merge_ydl_opts = {
                'format': f"{vf_choice}+{af_choice}",  # Select the chosen audio and video format
                'outtmpl': '%(title)s (merged).%(ext)s',  # Save with the video title
                'ext': vcodec_choice,  # Save merged format as selected video format
            }
            fetch(url_input, merge_ydl_opts)  # fetch and download
            break
        elif user_perm.lower() == "n":
            break
        else:
            print("Invalid input")
            continue

