
# # -----------------------------------
# # Python wave合并wav
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
append_wav("ask.wav", "record.wav", "all2.wav")

# import wave
#
# infiles = ["ask.wav", "record.wav"]
# outfile = "all.wav"
#
# data= []
# for infile in infiles:
#     w = wave.open(infile, 'rb')
#     data.append( [w.getparams(), w.readframes(w.getnframes())] )
#     w.close()
#
# output = wave.open(outfile, 'wb')
# output.setparams(data[0][0])
# output.writeframes(data[0][1])
# output.writeframes(data[1][1])
# output.close()