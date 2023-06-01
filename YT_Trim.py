from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.editor import VideoFileClip
import os

user = os.getlogin()

def download(link):
    try:
        yt = YouTube(link)
        yt = yt.streams.get_highest_resolution()
        filepath = yt.download(f"C:\\Users\\{user}\\Videos\\")
        filename = yt.default_filename
        print(f"You have downloaded: {filename}")
        return filepath
    except RegexMatchError:
        print("Error: Invalid link or video unavailable")

link = input("Enter URL: ")
filename = download(link)

cutchoice = input("Would you like to cut the video? Y/N: ")

while cutchoice != "Y" and cutchoice != "N":
    print("Invalid input")
    cutchoice = input("Would you like to cut the video? Y/N: ")

if cutchoice == "N":
    print("Finished")

elif cutchoice == "Y":
    timestart = int(input("What is the starting point in seconds: "))
    timeend = int(input("What is the ending point in seconds: "))
    video = VideoFileClip(filename)
    clip = video.subclip(timestart, timeend)
    output_name = input("What would you like the file name to be? (Do not include file extension): ")
    output_name = output_name + ".mp4"
    output_path = f"C:\\Users\\{user}\\Videos\\" + output_name
    clip.write_videofile(output_path)
    print(f"Trimmed video saved as {output_name}")
    clip.close()

keepchoice = input("Would you like to keep the full video? Y/N: ")

while keepchoice != "Y" and keepchoice != "N":
    print("Invalid input")
    keepchoice = input("Would you like to keep the full video? Y/N: ")

if keepchoice == "N":
    os.remove(filename)
    print("File deleted")

elif keepchoice == "Y":
    print("File kept")



