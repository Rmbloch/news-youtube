import datetime
from google.cloud import speech, storage
import os

def upload_audio_to_gcs(bucket_name, audio_file):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(os.path.basename(audio_file))
    blob.upload_from_filename(audio_file)

    blob.upload_from_filename(audio_file)
    print(
        "File {} uploaded to {}.".format(
            audio_file, blob.path
        )
    )
    return f"gs://{bucket_name}/{blob.name}"

def delete_audio_from_gcs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print(
        "File {} deleted from {}.".format(
            blob_name, bucket_name
        )
    )

def format_time(seconds):
    ms = int((seconds - int(seconds)) * 1000)
    time = str(datetime.timedelta(seconds=int(seconds)))
    return f"{time},{ms:03d}"

def split_transcript(transcript):
        words = transcript.split()
        segments = []
        current_segment = []

        for word in words:
            if len(" ".join(current_segment + [word])) <= 15:
                current_segment.append(word)
            else:
                segments.append(" ".join(current_segment))
                current_segment = [word]

        if current_segment:
            segments.append(" ".join(current_segment))

        return segments

def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    bucket_name = "news-audio-files"
    gcs_uri = upload_audio_to_gcs(bucket_name, audio_file)

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=300)

    srt_lines = []
    index = 1

    for result in response.results:
        for alternative in result.alternatives:
            words = alternative.words
            start_time = words[0].start_time
            end_time = words[0].end_time
            transcript = words[0].word

            for i in range(1, len(words)):
                word_info = words[i]
                new_transcript = transcript + " " + word_info.word
                if len(new_transcript) > 15:
                    segments = split_transcript(transcript)
                    segment_start_time = start_time
                    for segment in segments:
                        segment_end_time = end_time if segment == segments[-1] else word_info.start_time
                        srt_lines.append(f"{index}")
                        srt_lines.append(f"{format_time(segment_start_time.seconds + segment_start_time.microseconds * 1e-6)} --> {format_time(segment_end_time.seconds + segment_end_time.microseconds * 1e-6)}")
                        srt_lines.append(segment)
                        srt_lines.append("")
                        index += 1
                        segment_start_time = word_info.start_time
                    start_time = word_info.start_time
                    transcript = word_info.word
                else:
                    transcript = new_transcript
                    end_time = word_info.end_time

            if transcript:
                srt_lines.append(f"{index}")
                srt_lines.append(f"{format_time(start_time.seconds + start_time.microseconds * 1e-6)} --> {format_time(end_time.seconds + end_time.microseconds * 1e-6)}")
                srt_lines.append(transcript)
                srt_lines.append("")
                index += 1


    with open("subtitles.srt", "w") as srt_file:
        srt_file.write("\n".join(srt_lines))

    delete_audio_from_gcs(bucket_name, os.path.basename(audio_file))