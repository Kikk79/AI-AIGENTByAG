import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from google import genai
from dotenv import load_dotenv
import tempfile
import time

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

SILENCE_THRESHOLD = 2000  # Amplitude threshold for "silence" (Raised to ignore fan noise/static)
SILENCE_DURATION = 2.5   # Seconds of silence to trigger stop (Slightly reduced for snappier response)
MAX_DURATION = 20.0      # Safety cutoff (Reduced from 30)

def record_audio(fs=44100):
    """
    Records audio using VAD (Voice Activity Detection).
    Stops when silence_duration > 3s.
    """
    print("Listening... (Waiting for speech)")
    
    recording = []
    failed_silence_counter = 0
    speech_started = False
    start_time = time.time()
    last_sound_time = time.time()
    
    # Block size for stream (0.1s chunks)
    block_size = int(fs * 0.1) 
    
    with sd.InputStream(samplerate=fs, channels=1, dtype='int16') as stream:
        while True:
            # Read chunk
            data, overflow = stream.read(block_size)
            flattened = data.flatten()
            max_amp = np.max(np.abs(flattened))
            
            # Append to buffer
            recording.append(data)
            
            # Check for speech
            current_time = time.time()
            total_time = current_time - start_time
            
            if max_amp > SILENCE_THRESHOLD:
                if not speech_started:
                    print("   [Speech Detected] Recording...")
                    speech_started = True
                last_sound_time = current_time
            
            # Logic to stop
            silence_duration = current_time - last_sound_time
            
            # If we haven't started speaking, allowed to wait a bit, but basically we loop until speech or timeout
            if not speech_started:
                # If no speech for 10s wait, we return None (timeout)
                if total_time > 10.0:
                    return None, fs
                continue # Keep listening for start
            
            # If speech started, check for end silence
            if speech_started and silence_duration > SILENCE_DURATION:
                print(f"   [End of Turn] Silence detected ({SILENCE_DURATION}s).")
                break
                
            if total_time > MAX_DURATION:
                print("   [Limit Reached] Cutting off.")
                break

    # Concatenate all chunks
    full_recording = np.concatenate(recording, axis=0)
    
    # --- Normalization Logic (Same as before) ---
    max_amp_overall = np.max(np.abs(full_recording))
    print(f"   [Peak Level]: {max_amp_overall}")
    
    if max_amp_overall > 0:
        full_recording_float = full_recording.astype(np.float32)
        gain = 16000.0 / (max_amp_overall + 1.0)
        if gain > 50: gain = 50
        full_recording_float = full_recording_float * gain
        full_recording = np.clip(full_recording_float, -32767, 32767).astype(np.int16)

    return full_recording, fs

def transcribe_audio(audio_data, fs):
    """Saves to temp wav and sends to Gemini for transcription."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        wav.write(temp_wav.name, fs, audio_data)
        temp_wav_path = temp_wav.name

    try:
        with open(temp_wav_path, "rb") as f:
            audio_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                "Transcribe this audio exactly. Return ONLY the text, no other commentary.",
                genai.types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
            ]
        )
        return response.text.strip()
        
    except Exception as e:
        print(f"STT Error: {e}")
        return ""
    finally:
        try:
            os.remove(temp_wav_path)
        except:
            pass

if __name__ == "__main__":
    # Test
    audio, fs = record_audio()
    if audio is not None:
        text = transcribe_audio(audio, fs)
        print(f"You said: {text}")
