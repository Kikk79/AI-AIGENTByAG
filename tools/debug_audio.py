import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time

def list_devices():
    print("Available Audio Devices:")
    devices = sd.query_devices()
    print(devices)
    return devices

def test_recording():
    fs = 44100
    duration = 5
    print("\n------------------------------------------------")
    print(f"Recording 5 seconds test... Speak 'JARVIS' loud and clear.")
    print("------------------------------------------------")
    
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    
    # Check max amplitude
    max_amp = np.max(np.abs(recording))
    print(f"\nMax Amplitude detected: {max_amp} (Range: 0-32767)")
    
    if max_amp < 100:
        print("[WARNING] Microphone seems muted or very quiet!")
    elif max_amp < 1000:
        print("[WARNING] Audio is quite quiet. Might need gain.")
    else:
        print("[SUCCESS] Audio signal detected.")
        
    filename = "test_mic_output.wav"
    wav.write(filename, fs, recording)
    print(f"Saved to {filename}. Please play this file to verify you can hear yourself.")

if __name__ == "__main__":
    list_devices()
    test_recording()
