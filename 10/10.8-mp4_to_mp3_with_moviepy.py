from moviepy.editor import *
video_file_name = 'r7.mp4'
clip = VideoFileClip(video_file_name)
finalclip=clip.subclip(0,30)
finalclip.save_frame("frame.jpeg") # saves the first frame
audio = finalclip.audio
shape_data=audio.reader.buffer.shape

#这里可以根据shape_data,设计声音的数组
audio.write_audiofile(video_file_name.replace('.mp4','.mp3'))