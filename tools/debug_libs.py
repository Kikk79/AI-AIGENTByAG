import elevenlabs
from elevenlabs import ElevenLabs

print("ElevenLabs Module Dir:", dir(elevenlabs))
try:
    client = ElevenLabs(api_key="test")
    print("Client Dir:", dir(client))
except Exception as e:
    print(f"Client Init Error: {e}")
