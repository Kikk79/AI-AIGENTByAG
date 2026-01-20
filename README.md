# J.A.R.V.I.S. (AI Assistant)

**Just A Rather Very Intelligent System**

An advanced, locally running AI assistant inspired by Iron Man's J.A.R.V.I.S.
Built with **Google Gemini 2.0 Flash** (Brain) and **ElevenLabs** (Voice).

## 🚀 Features

*   **🎙️ Voice Interaction:** Fast Speech-to-Text (STT) and Text-to-Speech (TTS) with a sarcastic personality.
*   **🧠 Intelligent Agent:** Can "think" before acting, deciding whether to answer directly or use tools.
*   **👀 Vision:** Can see your screen! Just ask "Was siehst du?" (What do you see?).
*   **🦾 Automation:** Can open websites and launch applications on command.
*   **💾 Memory:** Remembers context across the conversation.
*   **🇩🇪 German Native:** Optimized for German language interaction.

## 🛠️ Installation

### Prerequisites
*   Python 3.10 or higher.
*   An API Key from [Google AI Studio](https://aistudio.google.com/) (Gemini).
*   An API Key from [ElevenLabs](https://elevenlabs.io/) (Voice).

### Windows
1.  Run `install_windows.bat`
2.  Edit the created `.env` file and add your API keys.
3.  Run `python jarvis.py`

### MacOS / Linux
1.  Make script executable: `chmod +x install_mac.sh`
2.  Run `./install_mac.sh`
3.  Edit the `.env` file with your keys.
4.  Run `python3 jarvis.py`

## 🕹️ Controls

*   **Wake Word:** "Jarvis", "Chavez", "Travis", etc.
*   **Continuous Mode:** After activation, he listens for 30 seconds for follow-up commands.
*   **Stop:** Say "Schalte dich ab" or press `Ctrl+C`.

## 📂 Project Structure

*   `jarvis.py`: Main entry point.
*   `tools/`: Capability modules (Listen, Speak, Think, Vision, Automation).
*   `brain/`: Memory files (Markdown).

## ⚠️ Configuration

Ensure your `.env` file looks like this:
```ini
GEMINI_API_KEY=AIzaSy...
ELEVENLABS_API_KEY=sk_...
```
