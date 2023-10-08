import paddle
import os,subprocess
from paddlespeech.cli.tts import TTSExecutor
tts_executor = TTSExecutor()
head_file = "ask.wav"
text='请问什么是钝感力?'
wav_file = tts_executor(
    text=text,
    am='fastspeech2_aishell3',# TTS任务的声学模型 fastspeech2_aishell3  fastspeech2_csmsc
    voc='hifigan_csmsc',# TTS任务的声码器
    lang='zh',# TTS任务的语言
    spk_id=6,# 说话人ID
    use_onnx=True,
    output=head_file,
    cpu_threads=4)
print('Wave file has been generated: {}'.format(head_file))
# # os.system("mpg123 ask.wav")
# subprocess.call("mpg123 ask.wav", shell=True)