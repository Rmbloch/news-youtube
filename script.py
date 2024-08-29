import os
from moviepy.editor import AudioFileClip
from news import grab_articles
from groq_request import summarize_article, generate_description, generate_tags, generate_title_tiktok, generate_title_youtube
from text_to_speech import text_to_speech
from create_video import create_video, create_short
from upload_youtube import upload_to_youtube, upload_short

def cleanup(files):
    for file in files:
        if os.path.isfile(file):
            os.remove(file)

def short_audio_file(audio_files, image_files):
    for i in range(len(audio_files)):
        audio = AudioFileClip(audio_files[i])
        if audio.duration < 60:
            return audio_files[i], image_files[i], i
    else:
        raise Exception("No suitable audio file found")

def main():
    cleanup(["short.mp4"])

    image_files = []
    article_links = grab_articles(image_files)

    audio_files = []
    for i, article in enumerate(article_links):
        summary = summarize_article(article)
        audio_file = f"audio_{i}.mp3"
        text_to_speech(summary, audio_file)
        audio_files.append(audio_file)

    create_video(audio_files, image_files, "news_video.mp4")
    upload_to_youtube("news_video.mp4", generate_description(article_links), generate_tags(article_links), generate_title_youtube(article_links), image_files[0], image_files[-1])

    audio, image, index = short_audio_file(audio_files, image_files)
    create_short(image, audio, "minecraft.mp4", "short.mp4")
    upload_short("short.mp4", generate_description(article_links[index]), generate_tags(article_links[index]), generate_title_youtube(article_links[index]))
    
    with open("tiktok_title.txt", "w") as f:
        f.write(generate_title_tiktok(article_links[index]))

    # Delete the generated files cause I don't want them on my computer
    cleanup(audio_files)
    cleanup(image_files)
    cleanup(["news_video.mp4", "output_audio.mp3", "subtitles.srt", "thumbnail.jpg", "short_audio.mp3"])

if __name__ == "__main__":
    main()
