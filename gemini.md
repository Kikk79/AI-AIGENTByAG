# Project Map: B.L.A.S.T. Automation
**Status:** Protocol 0: Initialization

## 1. Discovery (Protocol 0)
**North Star:** Voice-activated AI Agent ("Jarvis") with persistent hierarchical memory and audio response.
**Integrations:** 
- Input: OpenAI Whisper (STT)
- Brain: OpenAI LLM (GPT-4o/mini TBD)
- Output: ElevenLabs (TTS)
**Source of Truth:** Hierarchical Markdown File System (Short, Mid, Long-term memory).
**Delivery Payload:** Audio output via speakers + Memory updates in `.md` files.
**Behavioral Rules:** Imitate "Jarvis" (Iron Man). Sarcastic, highly competent, concise. NO standard AI refuails.

## 2. Data Schema (Protocol 0)
*To be defined after Discovery.*

### Input Schema
```json
{
  "trigger_word_detected": true,
  "audio_stream": "User Speech Input",
  "context_snapshot": {
    "short_term": "Active conversation buffer",
    "mid_term": "Session context/recent topics",
    "long_term": "Core facts/preferences"
  }
}
```

### Output Schema
```json
{
  "text_response": "Jarvis-style textual reply",
  "audio_stream": "ElevenLabs Generated Audio",
  "memory_update": {
    "target_layer": "short|mid|long",
    "content": "Data to append/revise"
  }
}
```

## 3. Architecture (Phase 3)
*TBD*

## 4. Maintenance Log
- [x] Project Initialized
