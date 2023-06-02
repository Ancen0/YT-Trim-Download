from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.editor import VideoFileClip
from pathlib import Path
import sys


def validate_input(prompt):
    while True:
        choice = input(prompt)
        if choice == "Y" or choice == "N":
            return choice
        print("Invalid input")


class UserInput:
    def __init__(self):
        self.url = ""
        self.cut_choice = ""
        self.time_start = ""
        self.time_end = ""
        self.output_name = ""
        self.keep_choice = ""

    def get_input(self):
        self.url = input("Enter URL: ")
        self.cut_choice = validate_input("Would you like to trim the video? Y/N: ")

        if self.cut_choice == "Y":
            self.time_start = int(input("What is the starting point in seconds?: "))
            self.time_end = int(input("What is the ending point in seconds?: "))
            self.output_name = input("What would you like the file name to be? (Without file extension): ")
        elif self.cut_choice == "N":
            download_video(self.url)
            sys.exit()

        self.keep_choice = validate_input("Would you like to keep the full video? Y/N: ")


def download_video(video_name):
    try:
        current_user = Path.home().name
        yt = YouTube(video_name)
        yt = yt.streams.get_highest_resolution()
        download_path = Path(f"C:/Users/{current_user}/Videos/")
        download_path.mkdir(parents=True, exist_ok=True)
        filepath = yt.download(str(download_path))
        filename = yt.default_filename
        print(f"You have downloaded: {filename}")
        return filepath
    except RegexMatchError:
        print("Error: Invalid link or video unavailable")
        sys.exit()


user_input = UserInput()
user_input.get_input()

if user_input.cut_choice == "N":
    name = download_video(user_input.url)
    print(f"Video downloaded: {name}")
    sys.exit(1)

name = download_video(user_input.url)

cut_choice = user_input.cut_choice

time_start = user_input.time_start
time_end = user_input.time_end
video = VideoFileClip(name)
clip = video.subclip(time_start, time_end)
output_name = user_input.output_name + ".mp4"
user = Path.home().name
output_path = Path(f"C:/Users/{user}/Videos/") / output_name
clip.write_videofile(str(output_path))
print(f"Trimmed video saved as {output_name}")
clip.close()

keep_choice = user_input.keep_choice

if keep_choice == "Y":
    print("File kept")
elif keep_choice == "N":
    name_path = Path(name)
    name_path.unlink()
    print("File deleted")
