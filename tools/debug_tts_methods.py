from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="test")
print("TTS Dir:", dir(client.text_to_speech))
