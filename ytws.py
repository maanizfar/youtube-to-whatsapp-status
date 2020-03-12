#!/usr/bin/python3

import argparse
import subprocess
import math
import youtube_dl
import os
from shutil import rmtree
import re

parser = argparse.ArgumentParser()
parser.add_argument('url', help='url of youtube video', type=str)
parser.add_argument('-k', '--keep-original', help='keep downloaded youtube video', action='store_true')
parser.add_argument('-l', '--landscape', help='rotate video to landscape mode', action='store_true')
args = parser.parse_args()

ytd_opts = {'format': 'mp4', 'outtmpl': './temp/%(id)s.%(ext)s', }
with youtube_dl.YoutubeDL(ytd_opts) as ytd:
    video_info = ytd.extract_info(args.url, download=False)
    downloaded_video_id = video_info['id']
    downloaded_video_extension = video_info['ext']
    downloaded_video_title = video_info['title']
    print(downloaded_video_title)
    if os.path.exists('temp'):
        rmtree('temp')
    os.mkdir('temp')
    ytd.download([args.url,])

# video_length = subprocess.check_output(("ffprobe", 'video.mp4', '-show_entries', 'format=duration',\
#                                              '-of', 'default=noprint_wrappers=1:nokey=1', '-v', 'error')).strip()
video_length = int(video_info['duration'])
print(video_length)

numOfClips = int(math.ceil(video_length/30))
print(numOfClips)


for n in range(numOfClips):
    start_time = n * 30
    out_video_name = str('temp/{}-clip.{}'.format(n+1, downloaded_video_extension))
    print(out_video_name)

    rotate = ''
    if args.landscape:
        rotate = ' -vf "transpose=1"'    

    cmd = 'ffmpeg -i temp/{}.{} {} -ss {} -t 30 {}'.format(downloaded_video_id, downloaded_video_extension, rotate,start_time, out_video_name)

    subprocess.run(cmd, shell=True)

if not args.keep_original:
    os.remove('temp/{}.{}'.format(downloaded_video_id, downloaded_video_extension))


dirName = re.sub(r'\W+ ', '',downloaded_video_title)
if os.path.exists(dirName):
    rmtree(dirName)
os.rename('temp', dirName)