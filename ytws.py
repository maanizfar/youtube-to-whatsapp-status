#!/usr/bin/python3

import argparse
import subprocess
import math
import youtube_dl
import os
from shutil import rmtree
import re
import os.path

def create_temp_dir():
    path = os.path.join(os.getcwd(), 'temp')
    
    if not os.path.exists(path):
        os.mkdir(path)

    return path

def create_temp_video_dir(name):
    temp_dir = create_temp_dir()
    path = os.path.join(temp_dir, name)
   
    if os.path.exists(path):
        rmtree(path)
    os.mkdir(path)

    return path

def download_video(url, force):
    ytd_opts = {'format': 'mp4', 'outtmpl': './temp/%(id)s.%(ext)s', }
    with youtube_dl.YoutubeDL(ytd_opts) as ytd:
        video_info = ytd.extract_info(url, download=False)
        temp_dir = create_temp_dir()

        video_path = os.path.join(temp_dir, video_info['id']+'.'+video_info['ext'])
        if not force and os.path.exists(video_path):
            print(f'[ytws] Skipping download as {video_path} already exists')
        else:
            ytd.download([url,])
        return video_info

def split_video(in_video_path, out_video_path, start_time, duration):
        cmd = f'ffmpeg -loglevel warning -i {in_video_path} -ss {start_time} -t {duration} {out_video_path}'
        subprocess.call(cmd, shell=True)
        print(f'[ytws] Created: {out_video_path}')

def rotate_video(in_video_path, out_video_path):
        override = os.path.samefile(in_video_path, out_video_path)

        if override:
            out_video_name = os.path.splitext(out_video_path)[0]
            out_video_ext = os.path.splitext(out_video_path)[1]
            out_video_path = out_video_name + '-temp' + out_video_ext

        cmd = 'ffmpeg -loglevel warning -i {} -vf "transpose=1" {} -y'
        subprocess.call(cmd.format(in_video_path, out_video_path), shell=True)

        if override:
            os.rename(out_video_path, in_video_path)

        print(f'[ytws] Rotated: {in_video_path}')

def rename_and_move_folder(move_from, new_name):
    dir_name = re.sub(r'\W+ ', '', new_name)
    if os.path.exists(dir_name):
        rmtree(dir_name)
    os.rename(move_from, os.path.join(os.getcwd(), dir_name))
    return os.path.join(os.getcwd(), dir_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url of youtube video', type=str)
    parser.add_argument('-k', '--keep-original', help='keep downloaded youtube video', action='store_true')
    parser.add_argument('-l', '--landscape', help='rotate video to landscape mode', action='store_true')
    parser.add_argument('-t',  help='duration of clips, DEFAULT=30', type=float)
    parser.add_argument('-f', '--force-download', help='delete video if already downloaded and download new video.', action='store_true')
    args = parser.parse_args()

    downloaded_video = download_video(args.url, args.force_download)

    video_extension = downloaded_video['ext']
    video_id = downloaded_video['id']
    video_title = downloaded_video['title']
    video_length = int(downloaded_video['duration'])
    full_video_name = video_id+'.'+video_extension

    clip_duration = 30
    if args.t:
        clip_duration = args.duration
        
    num_of_clips = int(math.ceil(video_length/clip_duration))
    
    print(f'[ytws] Video name: {video_title}')
    print(f'[ytws] Video duration: {video_length} seconds')
    print(f'[ytws] Clips duration: {clip_duration} seconds')
    print(f'[ytws] Number of clips to be created: {num_of_clips}')
    
    temp_dir_path = create_temp_dir()
    temp_clips_path = create_temp_video_dir(video_id)

    for n in range(num_of_clips):
        start_time = n * clip_duration
        in_video_name = os.path.join(temp_dir_path, full_video_name)
        out_video_name = os.path.join(temp_clips_path, '{}-clip.{}'.format(n+1, video_extension))

        split_video(in_video_name, out_video_name, start_time, clip_duration)

        if(args.landscape):
            rotate_video(out_video_name, out_video_name)

    if not args.keep_original:
        os.remove(os.path.join(temp_dir_path, full_video_name))

    final_dir = rename_and_move_folder(temp_clips_path, video_title)
    print(f'[ytws] Find splitted clips at {final_dir}')

if __name__ == '__main__':
    main()