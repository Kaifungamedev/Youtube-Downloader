from pytube import Playlist
import os
import moviepy.editor as mp
import time
import requests
import eyed3
import tkinter


username = os.getlogin()


totaletime = 0.0
Desktop = os.path.expanduser("~/Desktop")


def calculate_time(start, end, formated=0.005) -> float:
    return format((end - start), str(formated) + "f")


def runner(playlist, mode='1'):
    if mode == '1':
        mp3(playlist)
    if mode == '2':
        print("curently unsuported")
    else:
        print('not a valid mode')


def mp3(playlist):
    global totaletime
    p = Playlist(str(playlist))
    print(p.title)
    folder = f"{Desktop}/{p.title}"

    for video in p.videos:
        # start timer{desktop}
        tic = time.perf_counter()
        # downloads video
        print("downloating:", video.title)
        vid = video.streams.filter(file_extension="mp4").first().download(folder)
        vid
        # download image
        img_data = requests.get(video.thumbnail_url).content
        with open(f"{folder}/cover.jpg", "wb") as handler:
            handler.write(img_data)
        # convert mp4 to mp3
        print("Converting : " + vid)
        mp4_path = os.path.join(folder, vid)
        mp3_path = os.path.join(folder, os.path.splitext(vid)[0] + ".mp3")
        new_file = mp.AudioFileClip(mp4_path)
        new_file.write_audiofile(mp3_path)
        os.remove(mp4_path)
        # add thumnail tp mp3
        safe_title = video.title.replace(".", "")
        audio = eyed3.load(f"{folder}/{str(safe_title)}.mp3")
        if audio.tag == None:
            audio.initTag()
        audio.tag.images.set(3, open(f"{folder}/cover.jpg", "rb").read(), "image/jpeg")
        audio.tag.save(version=eyed3.id3.ID3_V2_3)
        os.remove(f"{folder}/cover.jpg")
        # end timer
        toc = time.perf_counter()
        finaltime = calculate_time(tic, toc, 0.2)
        print(str(finaltime) + " sec")
        totaletime += float(finaltime)
    print(totaletime)





while True:
    runner(input("Youtube Playlist URL:"),input('mode\n 1:mp3\n 2:mp4\n'))
