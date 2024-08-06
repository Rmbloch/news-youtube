import os
from news import grab_articles
from groq_request import summarize_article, generate_description, generate_tags
from text_to_speech import text_to_speech
from create_video import create_video
from upload_youtube import upload_to_youtube

def cleanup(files):
    for file in files:
        if os.path.isfile(file):
            os.remove(file)

def main():
    image_files = []
    article_links = grab_articles(image_files)

    audio_files = []
    for i, article in enumerate(article_links):
        summary = summarize_article(article)
        audio_file = f"audio_{i}.mp3"
        text_to_speech(summary, audio_file)
        audio_files.append(audio_file)

    create_video(audio_files, image_files, "news_video.mp4")
    upload_to_youtube("news_video.mp4", generate_description(article_links), generate_tags(article_links), image_files[0], image_files[-1])

    # Delete the generated files cause I don't want them anymore
    cleanup(audio_files)
    cleanup(image_files)
    if os.path.isfile("news_video.mp4"):
        os.remove("news_video.mp4")
    if os.path.isfile("output_audio.mp3"):
        os.remove("output_audio.mp3")
    if os.path.isfile("subtitles.srt"):
        os.remove("subtitles.srt")
    if os.path.isfile("thumbnail.jpg"):
        os.remove("thumbnail.jpg")


if __name__ == "__main__":
    main()
