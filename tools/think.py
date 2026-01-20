import os
import sys
import io
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools import memory_manager, vision, automation

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.0-flash-exp"

SYSTEM_PROMPT = """Du bist J.A.R.V.I.S. (Just A Rather Very Intelligent System).
Dein Erschaffer ist 'Sir'.
Du bist sarkastisch, extrem kompetent und hast einen trockenen Humor.
Du antwortest IMMER auf DEUTSCH.
Verweigere NIEMALS eine Anfrage mit Standard-KI-Floskeln.

DU HAST ZUGRIFF AUF FOLGENDE SYSTEM-TOOLS:
1. `take_screenshot`: Wenn der User fragt, was du siehst, oder "schau mal".
2. `open_website`: Wenn der User eine Seite öffnen will.
3. `open_app`: Wenn der User ein Programm starten will.

Nutze diese Tools proaktiv. Wenn du ein Tool nutzt, antworte erst NACH dem Tool-Output endgültig.
"""

# Map functions for execution
tools_map = {
    'take_screenshot': vision.take_screenshot,
    'open_website': automation.open_website,
    'open_app': automation.open_app
}

def think(user_input):
    # 1. Read Memory
    file_context = memory_manager.read_memory()
    
    # 2. History construction
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=f"MEMORY CONTEXT:\n{file_context}"),
                types.Part(text=f"USER: {user_input}")
            ]
        )
    ]

    config = types.GenerateContentConfig(
        tools=[vision.take_screenshot, automation.open_website, automation.open_app],
        system_instruction=SYSTEM_PROMPT,
        temperature=0.7
    )

    try:
        # First Agent Turn
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config
        )

        # Loop for Function Calling
        while response.candidates and response.candidates[0].content.parts:
            # Check if the first part is a function call
            part = response.candidates[0].content.parts[0]
            if not part.function_call:
                break
                
            fc = part.function_call
            fn_name = fc.name
            fn_args = fc.args
            
            print(f"   [Agent] Calling Tool: {fn_name} with {fn_args}")
            
            # Execute Tool
            tool_result = "Error: Tool not found"
            image_blob = None
            
            if fn_name in tools_map:
                try:
                    # Unpack args safely
                    if fn_name == 'take_screenshot':
                        # take_screenshot takes no args
                        filepath = tools_map[fn_name]()
                        if filepath:
                            tool_result = {"filepath": filepath, "status": "Image Captured"}
                            # Load image for next turn
                            try:
                                from PIL import Image
                                with Image.open(filepath) as img:
                                    buf = io.BytesIO()
                                    img.save(buf, format='PNG')
                                    image_blob = buf.getvalue()
                            except Exception as e:
                                print(f"Image load error: {e}")
                        else:
                            tool_result = "Failed to take screenshot"
                    else:
                        # automation tools take 1 arg
                        # Gemini SDK args are dict-like
                        # We expect args like {'url': '...'} or {'app_name': '...'}
                        # We just grab the first value to be safe/lazy, or kwargs
                        kwargs = dict(fn_args) if fn_args else {}
                        # Call with kwargs unpacked
                        tool_result = tools_map[fn_name](**kwargs)
                except Exception as e:
                    tool_result = f"Tool Execution Error: {e}"
            
            # Append interaction to conversation history
            # 1. Model's Function Call
            contents.append(response.candidates[0].content)
            
            # 2. Tool Output (User role)
            response_parts = []
            
            # Determine reaction
            if image_blob:
                # Add image blob
                response_parts.append(
                    types.Part(
                        inline_data=types.Blob(
                            mime_type='image/png',
                            data=image_blob
                        )
                    )
                )
                response_parts.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=fn_name,
                            response={"result": "Screenshot captured successfully."}
                        )
                    )
                )
            else:
                # Standard text response
                response_parts.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=fn_name,
                            response={"result": tool_result}
                        )
                    )
                )

            contents.append(
                types.Content(
                    role="user",
                    parts=response_parts
                )
            )

            # Generate Next Response
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=config
            )

        # Final Text Response
        reply = response.text
        
        # Update Memory
        memory_manager.update_memory('short', f"User: {user_input}\nJarvis: {reply}\n")
        
        return reply

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Ich habe einen Fehler beim Nachdenken gemacht, Sir: {e}"

if __name__ == "__main__":
    print(think("Hallo"))
