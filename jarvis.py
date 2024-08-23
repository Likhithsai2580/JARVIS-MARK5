import threading
from backend.modules.automodel import Operate
from backend.modules.basic.listenpy import Listen

import mtranslate as mt
from threading import Lock
import os
import eel
import pyautogui

import base64
from backend.modules.extra import GuiMessagesConverter, LoadMessages
from dotenv import load_dotenv

def run_docker():
    import os
    os.chdir("backend/AI/Perplexica")
    os.system("docker compose up -d")

thread = threading.Thread(target=run_docker)
thread.start()

load_dotenv()
state = 'Available...'
messages = LoadMessages()
WEBCAM = False
js_messageslist = []
working: list[threading.Thread] = []
InputLanguage = os.environ['InputLanguage']
Username = os.environ['NickName']
lock = Lock()

def UniversalTranslator(Text: str) -> str:
    """Translates text to English."""
    english_translation = mt.translate(Text, 'en', 'auto')
    return english_translation.capitalize()

def MainExecution(Query: str):
    """Main execution function for handling user queries."""
    global WEBCAM, state
    Query = UniversalTranslator(Query) if 'en' not in InputLanguage.lower() else Query.capitalize()

    if state != 'Available...':
        return
    state = 'Thinking...'
    Decision = Operate(Query)

    if 'realtime-webcam' in Decision:
        python_call_to_start_video()
        print('Video Started')
        WEBCAM = True
    elif 'close_webcam' in Decision:
        print('Video Stopped')
        python_call_to_stop_video()
        WEBCAM = False

    return Decision

@eel.expose
def js_messages():
    """Fetches new messages to update the GUI."""
    global messages, js_messageslist
    with lock:
        messages = LoadMessages()
    if js_messageslist != messages:
        new_messages = GuiMessagesConverter(messages[len(js_messageslist):])
        js_messageslist = messages
        return new_messages
    return []

@eel.expose
def js_state(stat=None):
    """Updates or retrieves the current state."""
    global state
    if stat:
        state = stat
    return state

@eel.expose
def js_mic(transcription):
    """Handles microphone input."""
    print(transcription)
    if not working:
        work = threading.Thread(target=process_input, args=(transcription,), daemon=True)
        work.start()
        working.append(work)
    else:
        if working[0].is_alive():
            return
        working.pop()
        work = threading.Thread(target=process_input, args=(transcription,), daemon=True)
        work.start()
        working.append(work)

def process_input(transcription):
    global WEBCAM
    result = MainExecution(transcription)
    if result == "close_webcam":
        print('Video Stopped')
        python_call_to_stop_video()
        WEBCAM = False

@eel.expose
def python_call_to_start_video():
    """Starts the video capture."""
    eel.startVideo()

@eel.expose
def python_call_to_stop_video():
    """Stops the video capture."""
    eel.stopVideo()

@eel.expose
def python_call_to_capture():
    """Captures an image from the video."""
    eel.capture()

@eel.expose
def handle_captured_image(image_data):
    """Handles the captured image data from the web interface."""
    js_capture(image_data)

@eel.expose
def js_page(cpage=None):
    """Navigates to the specified page."""
    if cpage == 'home':
        eel.openHome()
    elif cpage == 'settings':
        eel.openSettings()

@eel.expose
def setup():
    """Sets up the GUI window."""
    pyautogui.hotkey('win', 'up')

@eel.expose
def js_language():
    """Returns the input language."""
    return str(InputLanguage)

@eel.expose
def js_assistantname():
    """Returns the assistant's name."""
    return "JARVIS"

@eel.expose
def js_capture(image_data):
    """Saves the captured image."""
    image_bytes = base64.b64decode(image_data.split(',')[1])
    with open('capture.png', 'wb') as f:
        f.write(image_bytes)

# Initialize Eel and start the application
eel.init('web')
eel.start('spider.html', port=44444)