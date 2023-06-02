from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.editor import VideoFileClip
import os
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
        user = os.getlogin()
        yt = YouTube(name)
        yt = yt.streams.get_highest_resolution()
        filepath = yt.download(f"C:\\Users\\{user}\\Videos\\")
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

user = os.getlogin()
timestart = user_input.timestart
timeend = user_input.timeend
video = VideoFileClip(name)
clip = video.subclip(timestart, timeend)
output_name = user_input.output_name + ".mp4"
output_path = f"C:\\Users\\{user}\\Videos\\" + output_name
clip.write_videofile(output_path)
print(f"Trimmed video saved as {output_name}")
clip.close()

keepchoice = user_input.keepchoice

if keepchoice == "Y":
    print("File kept")
elif keepchoice == "N":
    os.remove(name)
    print("File deleted")




