This script downloads youtube video using youtube-dl and splits it into 30 seconds parts using ffmpeg.


## Usage:
ytws.py [-h] [-k] [-l] url

##### positional arguments:
    url                   url of youtube video

##### optional arguments:


    -h  --help              show this help message and exit
    -t  DURATION            duration of clips, DEFAULT=30
    -k  --keep-original     keep downloaded youtube video
    -l  --landscape         rotate clips to landscape mode
    -f  --force-download    delete video if already downloaded and download the video again


## Required packages:
* youtube-dl
* ffmpeg
