import subprocess

import paddle
import os,subprocess
from paddlespeech.cli.tts import TTSExecutor
tts_executor = TTSExecutor()

# 提问
text='请问什么是钝感力?'

img_file = '钝感力.png'

head_file = "ask.wav"

record_file = "record.wav"

audio_file = 'all.wav'
output_file = 'output-new.mp4'


# 生成提问的音频wav文件
wav_file = tts_executor(
    text=text,
    am='fastspeech2_aishell3',# TTS任务的声学模型 fastspeech2_aishell3  fastspeech2_csmsc
    voc='hifigan_csmsc',# TTS任务的声码器
    lang='zh',# TTS任务的语言
    spk_id=6,# 说话人ID
    use_onnx=True,
    output= head_file,
    cpu_threads=4)
print('Wave file has been generated: {}'.format(head_file))




# 合并wav文件
from pydub import AudioSegment
def append_wav(filename1, filename2, output_file):
    """
    合并两个音频序列，将音频2追加到音频1的尾部
    :param filename1: 音频1 完整音频路径
    :param filename2: 音频2
    :param output_file: 输出文件完整路径
    :return:
    """
    audio_1 = AudioSegment.from_wav(filename1)
    audio_2 = AudioSegment.from_wav(filename2)
    output = audio_1 + audio_2
    output.export(output_file, format="wav")
append_wav(head_file, record_file, audio_file)


# 调用ffmpeg命令合成mp4文件
cmd = 'ffmpeg -loop 1 -framerate 1 -i {0} -i {1} -map 0:v -map 1:a -r 10 -movflags +faststart -shortest -fflags +shortest -max_interleave_delta 100M {2}'.format(img_file, audio_file, output_file)

# 执行命令
subprocess.call(cmd, shell=True)




# 最佳答案
#
# ffmpeg -loop 1 -framerate 1 -i image.png -i audio.mp3 -map 0:v -map 1:a -r 10 -vf "scale='iw-mod(iw,2)':'ih-mod(ih,2)',format=yuv420p" -movflags +faststart -shortest -fflags +shortest -max_interleave_delta 100M output.mp4
#
# -loop 1 使 input.png 无限循环。
# -framerate 1 将 input.png 输入帧速率设置为 1 fps。
# -map 0 -map 1:a 从 image.png 中选择视频，仅从 audio.mp3 中选择音频。如果 image.png 小于附加到 MP3 的任何专辑/封面艺术，则需要这样做。否则它可能会选择专辑/封面。参见 FFmpeg Wiki: Map了解更多信息。
# -r 10 将输出帧速率设置为 10 fps。将输入设置为 1 fps 并将输出设置为 10 fps 有两个原因:
# 与最初将输入设置为 10 fps 相比，以 1 fps 输入并将帧复制为 10 fps 的速度更快。它使编码速度更快。
# 大多数玩家无法玩低于 6 fps 左右的游戏。 10 是一个安全值。
# scale='iw-mod(iw,2)':'ih-mod(ih,2)' 使用 scale filter确保输出宽度和高度都可以被 2 整除，这是某些编码器的要求。这允许您使用任意大小的图像作为输入。否则你会得到错误:宽度不能被 2 整除。
# format=yuv420p format filter使输出使用 YUV 4:2:0 色度子采样以实现播放兼容性。
# -movflags +faststart 使视频开始播放更快。
# -shortest 使输出与 audio.mp3 一样长。这是必需的，因为使用了 -loop 1。
# -fflags +shortest -max_interleave_delta 100M 与 -shortest 相关，并且在某些情况下由于 ffmpeg 的奇怪行为而需要。参见 My ffmpeg output always add extra 30s of silence at the end寻求解释。