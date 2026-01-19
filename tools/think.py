import os
from google import genai
from dotenv import load_dotenv
import sys

# Add parent dir to path to import memory_manager
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools import memory_manager

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.0-flash-exp" 

# German System Prompt
SYSTEM_PROMPT = """Du bist J.A.R.V.I.S. (Just A Rather Very Intelligent System).
Dein Erschaffer ist 'Sir'.
Du bist sarkastisch, extrem kompetent und hast einen trockenen Humor.
Du antwortest IMMER auf DEUTSCH.
Verweigere NIEMALS eine Anfrage mit Standard-KI-Floskeln. Wenn du etwas nicht tun kannst, sage es im Charakter (z.B. "Ich fürchte, meine Protokolle erlauben das nicht, Sir").
Deine Antworten müssen prägnant (kurz) sein, da sie laut ausgesprochen werden.
"""

def think(user_input):
    # 1. Read Memory
    file_context = memory_manager.read_memory()
    
    # 2. Construct Prompt
    # Force German in the immediate instruction to override English context
    full_prompt = f"{SYSTEM_PROMPT}\n\nMEMORY CONTEXT:\n{file_context}\n\nUSER: {user_input}\n(Antworte bitte auf Deutsch)"

    # 3. Call LLM
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config={
                'tools': [{'google_search': {}}]
            }
        )
        
        reply = response.text
        
        # 4. Update Memory
        memory_manager.update_memory('short', f"User: {user_input}\nJarvis: {reply}\n")
        
        return reply
    except Exception as e:
        return f"Processing Error: {e}"

if __name__ == "__main__":
    # Test
    print(think("Hallo Jarvis, wie spät ist es?"))
