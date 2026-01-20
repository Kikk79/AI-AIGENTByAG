import os
import webbrowser
import subprocess
import platform

def open_website(url: str):
    """Opens a website in the default browser."""
    print(f"   [Auto] Opening URL: {url}")
    if not url.startswith('http'):
        url = 'https://' + url
    webbrowser.open(url)
    return f"Website opened: {url}"

def open_app(app_name: str):
    """
    Attempts to open an application.
    Basic implementation for Windows.
    """
    print(f"   [Auto] Launching: {app_name}")
    try:
        if platform.system() == "Windows":
            # Simple start for common apps or known paths
            # This is a bit "blind" but works for global commands
            os.startfile(app_name) 
        else:
            subprocess.Popen([app_name])
        return f"App launched: {app_name}"
    except Exception as e:
        return f"Failed to launch {app_name}: {e}"
