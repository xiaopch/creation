
# https://gitee.com/mirrors/openai-whisper.git 将其clone到本地
# 执行命令：python setup.py install

import whisper
import arrow
from zhconv import convert
from datetime import datetime
import os
from moviepy.editor import *

# 定义模型、音频地址、录音开始时间
def excute_asr(model_name,file_path,start_time):
    print('开始音频转文字:\n')
    model = whisper.load_model(model_name)
    result = model.transcribe(file_path,fp16=False, language='Chinese')

    filename = datetime.now().strftime('ASR_%Y_%m_%d_%H%M%S.md')
    print(filename)
    with open(filename,'w') as fh:
        fh.write('## {}\n'.format(title))
        fh.write('```\n')

        for segment in result["segments"]:
            now = arrow.get(start_time)
            start = now.shift(seconds=segment["start"]).format("YYYY-MM-DD HH:mm:ss")
            end = now.shift(seconds=segment["end"]).format("YYYY-MM-DD HH:mm:ss")
            # line ="【"+start+"->" +end+"】：" + convert(segment['text'], 'zh-cn')
            line ="【"+start+"】：" + convert(segment['text'], 'zh-cn')
            print(line)
            fh.write(line+'\n')
        fh.write('```')

def extract_audio_from_video(video_file_name,audio_file_name):
    clip = VideoFileClip(video_file_name)
    audio = clip.audio
    shape_data=audio.reader.buffer.shape
    #这里可以根据shape_data,设计声音的数组
    audio.write_audiofile(audio_file_name)
if __name__ == '__main__':

    print(datetime.now())

    video_file_name = str(input("请输入视频文件名:"))
    title = video_file_name.replace('.mp4','')
    audio_file_name = video_file_name.replace('.mp4','.mp3')
    if os.path.exists(audio_file_name):
        os.remove(audio_file_name)

    extract_audio_from_video(video_file_name,audio_file_name)

    excute_asr("small",audio_file_name,datetime.now())
