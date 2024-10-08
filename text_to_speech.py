from google.cloud import texttospeech

def text_to_speech(text, output_file):
    client = texttospeech.TextToSpeechClient()
    text_with_pause = text + '......'
    input_text = texttospeech.SynthesisInput(text=text_with_pause)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Journey-F", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
