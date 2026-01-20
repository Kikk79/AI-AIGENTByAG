import os
from PIL import ImageGrab
from datetime import datetime

SCREENSHOT_DIR = os.path.join(os.getcwd(), ".tmp", "vision")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot():
    """
    Captures the current screen and saves it to a temporary file.
    Returns the absolute path to the screenshot.
    """
    try:
        screenshot = ImageGrab.grab()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        screenshot.save(filepath)
        print(f"   [Vision] Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"   [Vision] Error: {e}")
        return None
