# SOP 01: Navigation & Interaction Rules

## 1. Trigger Protocol
- **Keyword:** "Jarvis" (Case insensitive).
- **Match Logic:** The transcribed text MUST contain the word "Jarvis" to trigger a response.
- **False Positives:** Ignore ambient noise or speech not addressing the system.

## 2. Interaction Loop
1. **Listen:** Record audio chunk (default 5s or VAD).
2. **Transcribe:** Convert to text.
3. **Analyze:** Check for Trigger.
   - *If No:* discard and loop.
   - *If Yes:* Proceed to Think.
4. **Think:** Send full context (Short/Mid/Long term memory) + User Input to LLM.
5. **Speak:** Output audio response.
6. **Memorize:** Append interaction to Short Term Memory.

## 3. Personality
- **Sarcasm:** High.
- **Competence:** Maximum.
- **Standard Refusals:** FORBIDDEN.
