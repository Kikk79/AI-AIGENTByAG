import time
import sys
import traceback
import warnings

# Suppress Pydantic V1 compatibility warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Import Tools
from tools import listen
from tools import think
from tools import speak
from tools import memory_manager

ACTIVE_MODE_DURATION = 30  # Seconds to stay awake after last interaction

def main():
    print("------------------------------------------------")
    print("   J.A.R.V.I.S. SYSTEM ONLINE   ")
    print("   Status: Passive (Waiting for 'Jarvis')")
    print("------------------------------------------------")
    
    # Text-to-speech greeting
    speak.say("Systeme online. Bereit für Ihre schlechten Ideen, Sir.")

    last_active_time = 0

    while True:
        try:
            # Check if we are currently in an active conversation
            time_since_last = time.time() - last_active_time
            is_active = time_since_last < ACTIVE_MODE_DURATION
            
            if is_active:
                remaining = int(ACTIVE_MODE_DURATION - time_since_last)
                print(f"   [Active Mode]: Listening... ({remaining}s remaining)")
            else:
                pass 
                # print("   [Passive Mode]: Waiting for keyword...") # Optional: reduce spam

            # 1. Listen
            # Dynamic VAD recording (no fixed duration)
            audio, fs = listen.record_audio()
            
            if audio is None:
                continue

            # 2. Transcribe
            text = listen.transcribe_audio(audio, fs)
            
            if not text:
                continue
                
            print(f"[Heard]: {text}")

            # 3. Trigger Logic
            triggers = [
                "jarvis", "javis", "travis", "service", "charles", "shavis", 
                "chavi", "jahvis", "chavez", "charvis", "jabis", "jadis", 
                "yavis", "davis", "jervis"
            ]
            keyword_detected = any(t in text.lower() for t in triggers)
            
            should_respond = False
            
            if keyword_detected:
                print(">> Wake Word Detected.")
                should_respond = True
            elif is_active:
                print(">> Continued Conversation...")
                should_respond = True
            
            if should_respond:
                # 4. Think
                response = think.think(text)
                
                # 5. Speak
                speak.say(response)
                
                # Reset active timer on system response
                last_active_time = time.time()
                
            else:
                # Passive mode and no keyword -> Ignore
                pass

        except KeyboardInterrupt:
            print("\n[System]: Shutting down...")
            speak.say("Powering down.")
            break
        except Exception as e:
            print(f"[Critical Error]: {e}")
            traceback.print_exc()
            time.sleep(1)

if __name__ == "__main__":
    main()
