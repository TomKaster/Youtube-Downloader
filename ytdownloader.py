import os
from pydub import AudioSegment
from pytube.cli import on_progress
from pytube import YouTube

def get_stream_highest_resolution():
    stream = YouTube(f'{url}', on_progress_callback=on_progress).streams.get_highest_resolution()
    run_download(stream)

def get_stream_itag(itag):
    stream = YouTube(f'{url}', on_progress_callback=on_progress).streams.get_by_itag(f'{itag}')
    run_download_audio(stream)

def run_download(stream):
    print('Connecting...')
    title = stream.title
    print(title)
    stream.download(output_path = f"{os.getenv('USERPROFILE')}\\Downloads")
    print("Finished downloading to your 'Downloads' folder.")
    input('Press Enter to exit')
    exit()

def run_download_audio(stream):
    print('Connecting...')
    title = stream.title
    print(title)
    stream.download(output_path = f"{os.getenv('USERPROFILE')}\\Downloads", filename = (f'{title}.webm'))
    convert_to_mp3(title)

def convert_to_mp3(title):
    AudioSegment.from_file(f"{os.getenv('USERPROFILE')}\\Downloads\\{title}.webm").export(f"{os.getenv('USERPROFILE')}\\Downloads\\{title}.mp3", format="mp3")
    os.remove(f"{os.getenv('USERPROFILE')}\\Downloads\\{title}.webm")
    print("Finished downloading to your 'Downloads' folder.")
    input('Press Enter to exit')
    exit()

answer = input("Do you want to download video or audio? Type 'video' or 'audio': ")
if answer == 'video':
    url = input('Enter the URL for the Youtube video you want to download: ')
    get_stream_highest_resolution()

elif answer == 'audio':
    url = input('Enter the URL for the Youtube video whose audio you want to download: ')
    get_stream_itag(251)
