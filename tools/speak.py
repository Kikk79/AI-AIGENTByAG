import os
import sounddevice as sd
import soundfile as sf
import io
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def say(text):
    if not text:
        return

    print(f"[Jarvis]: {text}")
    
    try:
        # Generate audio
        # Using a specific voice ID ideally, or first available.
        # "Brian" is a good Jarvis-like voice if available, or just default.
        # We'll use the first one or a hardcoded ID if known.
        # For now, let's pick "Rachel" or similar common one, or just let default pick.
        # We will use 'eleven_turbo_v2' for speed.
        
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb", # "George" - British, Warm (Jarvis-like)
            model_id="eleven_turbo_v2_5", # Optimized for latency
            output_format="mp3_44100_128",
        )
        
        # Consume generator if needed or convert to bytes
        audio_bytes = b"".join(audio_stream)
        
        # Play audio
        data, samplerate = sf.read(io.BytesIO(audio_bytes))
        sd.play(data, samplerate)
        sd.wait()
        
    except Exception as e:
        print(f"TTS Error: {e}")

if __name__ == "__main__":
    say("Greetings, Sir. Systems are online.")
