import os
import openai
import speech_recognition as sr
import pyaudio
from io import BytesIO
from google.cloud import texttospeech
openai.api_key = "Your own api key here"

client = texttospeech.TextToSpeechClient()
r = sr.Recognizer()

def main():

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Say something!")

        audio = r.listen(source)

        completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "user", "content": r.recognize_google(audio, language="en")}
          ]
        )

        try:
            response = completion.choices[0].message['content']
            audioconfig = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16
            )
            voiceconfig = texttospeech.VoiceSelectionParams(
                language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
            speechresponse = client.synthesize_speech(
                input=texttospeech.SynthesisInput(text=str(response)),
                voice=voiceconfig,
                audio_config=audioconfig,
            )

            audiospeechresponse = BytesIO(speechresponse.audio_content)
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(2), channels=1, rate=24000, output=True)
            stream.write(audiospeechresponse.getvalue())
            stream.close()
            p.terminate()
            print("Response \n" + str(response))

        except Exception as e:
            print("Error :  " + str(e))

        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())


if __name__ == "__main__":
    main()


