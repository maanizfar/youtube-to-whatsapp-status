This script downloads youtube video using youtube-dl and splits it into 30 seconds parts using ffmpeg.


## Usage:
ytws.py [-h] [-k] [-l] url

##### positional arguments:
    url                   url of youtube video

##### optional arguments:


    -h, --help           show this help message and exit
    -k, --keep-original  keep downloaded youtube video
    -l, --landscape      rotate video to landscape mode


## Required packages:
* youtube-dl
* ffmpeg
