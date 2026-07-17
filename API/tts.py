from dotenv import load_dotenv
import os
from google import genai
import wave
import base64
load_dotenv()  # Loads variables from .env

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")  # or os.getenv("GOOGLE_API_KEY")
)
def TTS(text):
    def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)
    interaction = client.interactions.create(
        model="gemini-3.1-flash-tts-preview",
        input=text,
        response_format={"type": "audio"},
        generation_config={
            "speech_config": [
                {"voice": "Kore"}
            ]
        }
    )

    wave_file("out.wav", base64.b64decode(interaction.output_audio.data))

