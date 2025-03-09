import os
import io
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from pydub.playback import play

# Load API key from .env file
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

# Initialize Eleven Labs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_play(text: str, voice_id: str):
    """
    Converts text to speech and plays it directly without saving as a file.

    Args:
        text (str): The text to convert to speech.
        voice_id (str): The ID of the Eleven Labs voice to use.
    """
    # Call Eleven Labs API for text-to-speech
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Collect audio data in memory (instead of saving to a file)
    audio_data = b"".join(chunk for chunk in response if chunk)

    # Convert binary audio data to a playable format
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")

    # Play the audio
    play(audio_segment)

if __name__ == "__main__":
    text_to_speech_play("Hello, world! This is a test of the Eleven Labs API.", "pNInz6obpgDQGcFmaJgB")