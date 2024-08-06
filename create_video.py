import os
import random
from moviepy.editor import AudioFileClip, VideoFileClip, ImageClip, concatenate_videoclips, CompositeVideoClip, concatenate_audioclips, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": "/usr/bin/convert"})
from pytubefix import YouTube
from subtitle import transcribe_audio

def create_video(audio_files, image_files, output_file):
    if not os.path.exists("minecraft.mp4"):
        yt = YouTube("https://www.youtube.com/watch?v=n_Dv4JMiwK8")
        yt.streams.filter(res="1080p").first().download(filename="minecraft.mp4")

    video = VideoFileClip("minecraft.mp4").without_audio()

    clips = []
    audio_clips = []
    for i in range(len(audio_files)):
        audio = AudioFileClip(audio_files[i])
        image = ImageClip(image_files[i]).set_duration(audio.duration)
        clips.append(image)
        audio_clips.append(audio)

    image_video = concatenate_videoclips(clips)
    audio_track = concatenate_audioclips(audio_clips)

    max_start_time = video.duration - image_video.duration
    start_time = random.uniform(0, max_start_time)
    video_subclip = video.subclip(start_time, start_time + image_video.duration)
    image_resize = image_video.resize(0.8)
    audio_track.write_audiofile("output_audio.mp3", bitrate='320k')
    #transcribe_audio("output_audio.mp3")
    #generator = lambda txt: TextClip(txt, font='Arial-Bold', fontsize=70, color='white', stroke_color='black', stroke_width=1)
    #subtitles = SubtitlesClip("subtitles.srt", generator)
    final_clip = CompositeVideoClip([video_subclip, image_resize.set_position(('right', 'top'))])
    final_clip = final_clip.set_audio(audio_track)
    final_clip.write_videofile(output_file, fps=60, bitrate='9000k', codec='libx264', audio_codec='aac')

