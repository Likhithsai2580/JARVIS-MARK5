import threading
from backend.modules.automodel import Operate
from backend.modules.basic.listenpy import Listen
from backend.modules.speak.speakmid import speakon
from backend.modules.speak.speakoff import speakoff

def run_docker():
    import os
    os.chdir("backend/AI/Perplexica")
    os.system("docker compose up -d")

thread = threading.Thread(target=run_docker)
thread.start()

while True:
    response = Listen()
    response = Operate(response)
    try:
        speakon(response)
    except:
        speakoff(response)