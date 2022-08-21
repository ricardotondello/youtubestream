from pytube import YouTube
from pytube.cli import on_progress
import moviepy.editor as mp
import os

def on_complete(stream, filepath):
    global is_only_audio
    print(f'\nDownload finished!\n')
    if is_only_audio:
        print("converting to MP3\n")
        convert_to_mp3(filepath)
    else:
        print(filepath)

def convert_to_mp3(filepath):
    mp4_path = filepath
    mp3_path = os.path.splitext(filepath)[0] + '.mp3'
    new_file = mp.AudioFileClip(mp4_path)
    new_file.write_audiofile(mp3_path)
    os.remove(mp4_path)
    print(mp3_path)

link = input("Provide the YouTube link: ")

yt = YouTube(link, on_progress_callback=on_progress, on_complete_callback=on_complete)

print(f'Title: {yt.title}')
print(f'Length: {yt.length} seconds')
print(f"Views: {yt.views:,}")

audios = yt.streams.filter(only_audio=True).order_by('abr').desc()
videos = yt.streams.filter(progressive=True).order_by('abr').desc()

print("\nAvailiable audios:")
for s in audios:
    print(f'{s.itag} - Quality: {s.abr}')

print("\nAvailiable videos:")
for s in videos:
    print(f'{s.itag} - Quality: {s.abr}')

selected_id = input("Choose beteween available downloads: ")

if(not selected_id.isnumeric()):
    print("Invalid selection, please try it again.")
    exit(1)

download_obj = yt.streams.get_by_itag(selected_id)

is_only_audio = not download_obj.is_progressive

download_obj.download()