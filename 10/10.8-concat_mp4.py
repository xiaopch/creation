from moviepy.editor import *
import os
from glob import glob



#定义合并的视频


video_list = []
files_list = glob('*.png.mp4')

mp4_file = 'mp4.txt'
outfile = 'o123.mp4'
with open(mp4_file,'w') as f:
    for file in glob('*.png.mp4'):
        f.write('file ' + '\''+file+'\'\n')



os.system('ffmpeg.exe -f concat -safe 0 -i {} -c copy -y {}'.format(mp4_file,outfile))
#