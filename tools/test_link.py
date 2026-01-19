import os
import openai
from dotenv import load_dotenv
import sounddevice as sd
import numpy as np
from elevenlabs.client import ElevenLabs

# Load Env
load_dotenv()
print("1. Environment Variables Loaded.")

# Test OpenAI
print("\n2. Testing OpenAI Connection...")
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI()
    response = client.models.list()
    print("   [SUCCESS] OpenAI Connected. Available models retrieved.")
except Exception as e:
    print(f"   [FAILURE] OpenAI Error: {e}")

# Test ElevenLabs
print("\n3. Testing ElevenLabs Connection...")
try:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client_eleven = ElevenLabs(api_key=api_key)
    # Using 'voices' property instead of method if applicable, or get_voices
    # The client structure varies by version, trying standard list
    voices = client_eleven.voices.get_all()
    print(f"   [SUCCESS] ElevenLabs Connected. Found {len(voices.voices)} voices.")
except Exception as e:
    print(f"   [FAILURE] ElevenLabs Error: {e}")

# Test Audio Output
print("\n4. Testing Audio Output (Speakers)...")
try:
    fs = 44100  # Sample rate
    seconds = 1  # Duration of recording
    
    # Generate a simple beep sound
    t = np.linspace(0, seconds, int(fs * seconds), endpoint=False)
    frequency = 440  # 440 Hz (A4)
    audio = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    print("   Playing test sound...")
    sd.play(audio, fs)
    sd.wait()
    print("   [SUCCESS] Audio play command executed. (Did you hear a beep?)")
except Exception as e:
    print(f"   [FAILURE] Audio Output Error: {e}")

print("\n--- Diagnostic Complete ---")
