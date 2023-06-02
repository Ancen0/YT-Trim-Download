from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.editor import VideoFileClip
from pathlib import Path
import sys

class UserInput:
    def __init__(self):
        self.url = ""
        self.cutchoice = ""
        self.timestart = ""
        self.timeend = ""
        self.output_name = ""
        self.keepchoice = ""

    def get_input(self):
        self.url = input("Enter URL: ")
        self.cutchoice = self.validate_input("Would you like to trim the video? Y/N: ")

        if self.cutchoice == "Y":
            self.timestart = int(input("What is the starting point in seconds?: "))
            self.timeend = int(input("What is the ending point in seconds?: "))
            self.output_name = input("What would you like the file name to be? (Without file extension): ")
        elif self.cutchoice == "N":
            download_video(self.url)
            sys.exit()

        self.keepchoice = self.validate_input("Would you like to keep the full video? Y/N: ")

    def validate_input(self, prompt):
        while True:
            choice = input(prompt)
            if choice == "Y" or choice == "N":
                return choice
            print("Invalid input")


def download_video(name):
    try:
        user = Path.home().name
        yt = YouTube(name)
        yt = yt.streams.get_highest_resolution()
        download_path = Path(f"C:/Users/{user}/Videos/")
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

if user_input.cutchoice == "N":
    name = download_video(user_input.url)
    print(f"Video downloaded: {name}")
    sys.exit(1)

name = download_video(user_input.url)

cutchoice = user_input.cutchoice

timestart = user_input.timestart
timeend = user_input.timeend
video = VideoFileClip(name)
clip = video.subclip(timestart, timeend)
output_name = user_input.output_name + ".mp4"
user = Path.home().name
output_path = Path(f"C:/Users/{user}/Videos/") / output_name
clip.write_videofile(str(output_path))
print(f"Trimmed video saved as {output_name}")
clip.close()

keepchoice = user_input.keepchoice

if keepchoice == "Y":
    print("File kept")
elif keepchoice == "N":
    name_path = Path(name)
    name_path.unlink()
    print("File deleted")




