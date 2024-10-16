from backend.modules.search import SEARCH
from backend.modules.llms import AIClient, pure_llama3
from filter import filter_python
from backend.modules.Powerpointer.main import generate_powerpoint
from backend.AI.dealers import dealing
import cv2
import pyautogui
import logging
import pyperclip
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
from backend.modules.OF.screenshare import SCREENSHARE
from backend.modules.OF.eye import EYE
from backend.modules.codebrew import CodeBrew, codebrewPrompt, samplePrompt
from backend.modules.llms import pure_llama3 as LLM
import platform
import json
from backend.modules.speak.speakmid import TTS as speakon
from backend.modules.speak.speakoff import off as speakoff
from morefunctions import logic

def speak(text):
    try:
        speakon(text)
    except:
        speakoff(text)

def get_os_info():
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    return os_name + os_version + os_release

def get_extension_info():
    with open("extensions/config_all.json", 'r') as f:
        data = json.load(f)
    
    extensions_info = []
    for extension in data['extensions']:
        extension_info = {
            'name': extension['name'],
            'description': extension['description'],
            'parameters': extension['parameters']
        }
        extensions_info.append(extension_info)
    return extensions_info

extension_prompt = """
"""

prompt_main = """
Given the user query, identify and respond with the relevant tags from the following list: [realtime-webcam, automation, real-time-knowledge, img-dealing, website-dealing, screenshare, video-dealing, pdf-dealing, excel-dealing, powerpoint-dealing, chat, application-dev, web-app, click]. If the query involves multiple tasks, combine the appropriate tags with a plus sign. Respond with only the tags and nothing else.
Examples:
Query: "Read the selected PDF and summarize it."
Response: pdf-dealing+automation

Query: "I want to share the screen"
Response: screenshare

Query: "Open YouTube"
Response: automation

Query: "Make a portfolio"
Response: website-dealing

Query: "Who won the elections"
Response: real-time-knowledge

Query: "Download video from website"
Response: website-dealing

Query: "Study this video"
Response: video-dealing

Query: "Create a web application for task management"
Response: web-app

Query: "Develop a desktop app for note-taking"
Response: application-dev

Query: "Can you see what I'm holding?"
Response: realtime-webcam+img-dealing

Query: "Analyze the PDF and create a PowerPoint presentation based on it"
Response: pdf-dealing+powerpoint-dealing
"""

automation_prompt = """
Please write a Python script that satisfies user. The script should handle module installation automatically. It should first attempt to install any required modules using the os.system method. If the installation fails, it should try an alternative approach to install the modules.
Requirements:

Task Specification: Clearly define the task the script should perform (e.g., "scrape data from a website," "process a CSV file," etc.).
Module Installation:
Use os.system to run pip install commands for missing modules.
If os.system fails, attempt another approach (e.g., using subprocess module).
Error Handling: Ensure that the script does not break if module installation fails and provides helpful error messages.
Example of the Task: "The script should read a CSV file, process the data, and plot a graph using Matplotlib."

Generated Script Example:

python
Copy code
import os
import subprocess
import sys

# Specify the task: read CSV, process data, and plot using Matplotlib

def install_module(module_name):
    try:
        os.system(f"pip install {module_name}")
    except Exception as e:
        print(f"Failed to install {module_name} using os.system: {e}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {module_name} using subprocess: {e}")
            sys.exit(1)

def main():
    # List of required modules
    modules = ['pandas', 'matplotlib']
    
    # Install missing modules
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            print(f"{module} not found. Installing...")
            install_module(module)
    
    # Import modules after installation
    import pandas as pd
    import matplotlib.pyplot as plt

    # Task: Read CSV, process data, and plot
    try:
        data = pd.read_csv('data.csv')
        data['Value'].plot(kind='bar')
        plt.show()
    except Exception as e:
        print(f"An error occurred while processing the task: {e}")

if __name__ == "__main__":
    main()

You are provided with a list of extensions and their parameters at the start of conversation. These extensions are available as Python functions located in the extensions directory, with each extension having its own Python file named after the extension itself.
Each extension function can be invoked directly by calling its corresponding Python function. If the extension requires any input parameters, provide them as arguments to the function call.
Here's an example of how to use an extension:
Suppose you want to use the extension1 extension:
'''python
from extensions.extension1 import extension1
# If extension1 requires parameters, provide them as arguments
result = extension1(param1, param2)
'''
Replace param1, param2, etc., with the actual parameters required by the extension.
Now, feel free to utilize any extension whenever needed by providing corresponding Python code only.

it seems user is using
"""+get_os_info()+get_extension_info()

prompt_distiguisher_img = """
Please determine the user's intent based on their request:

Analyze Image: If the user is asking to analyze an image, identify if they are referring to an image from a camera or a screen. Respond with:

img_from_camera if the image is from a camera.
img_from_screen if the image is from a screen.
Generate Image: If the user is asking to generate an image, respond with:

generate_img.
Example User Requests:

'Can you see this' → img_from_camera
'can you say what i am holding' -> img_from_camera
'what is this on my screen.' → img_from_screen
'Create an image of a sunset.' → generate_img
if the request made by user is unclear (i.e confusion b/w camera and screen) respond with unclear_request
Use the provided examples as a guide to classify and respond to the user's request.
"""

powerpoint_distiguisher_prompt = """You are an advanced language model capable of working with PowerPoint presentations. Your responses should be based on the context provided by the user's request. To handle user requests accurately, determine whether the user is asking to:

Generate a New PowerPoint Presentation: If the user asks for help creating a new PowerPoint presentation, including generating slides, adding content, or creating a presentation from scratch, respond with generate_pptx.

Perform Tasks with an Existing PowerPoint File: If the user asks for help with tasks related to an existing PowerPoint file, such as modifying, editing, or analyzing an existing presentation, respond with task_with_pptx.

For example:

User asks: "Can you create a presentation on climate change?" → Response: generate_pptx
User asks: "Can you update the title slide of my existing presentation?" → Response: task_with_pptx
Always ensure that your response accurately reflects the user's needs based on whether they are creating a new presentation or working with an existing one."""

def run_codebrew(user_input):
    llm = LLM(
        verbose=True, 
        max_tokens=4096, 
        messages=samplePrompt(), 
        system_prompt=codebrewPrompt()
    )
    codebrew = CodeBrew(llm, keepHistory=True)
    while True:
        user_input = input(">>> ")
        response = codebrew.run(user_input)
        print(response)

def record_screen(video_filename='output.mp4', duration=20):
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    screen_size = pyautogui.size()
    fps = 20
    out = cv2.VideoWriter(video_filename, codec, fps, screen_size)

    print(f"Recording started. Will record for {duration} seconds...")
    
    start_time = time.time()
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
        
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

    out.release()
    cv2.destroyAllWindows()
    print(f"Recording completed. Video saved as {video_filename}")

def copy_url_from_browser():
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

def get_url_from_clipboard():
    try:
        url = pyperclip.paste()
        if url.startswith('http://') or url.startswith('https://'):
            return url
        else:
            print("Clipboard does not contain a valid URL.")
            return None
    except Exception as e:
        print(f"An error occurred while reading from clipboard: {e}")
        return None

def scrape_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            web = soup.prettify()
            return web
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def webscraper():
    copy_url_from_browser()
    url = get_url_from_clipboard()
    if url:
        web_content = scrape_website(url)
        if web_content:
            print("Web content successfully retrieved and stored in 'web' variable.")
            return web_content
        else:
            return("Failed to retrieve web content.")
    else:
        return("No valid URL found in clipboard.")

def take_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    print("Screenshot saved as 'screenshot.png'.")

def capture_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Error: Could not capture image.")
        return
    cv2.imwrite('captured_photo.jpg', frame)
    print("Photo saved as 'captured_photo.jpg'.")

def execute_code(code_str):
    success = None
    error = None
    try:
        local_namespace = {}
        exec(code_str, {}, local_namespace)
        success = local_namespace
    except Exception as e:
        error = str(e)
    return success, error

def automation(user_input):
    prompt = automation_prompt + user_input
    code = filter_python(pure_llama3(prompt))
    success, error = execute_code(code)
    if success:
        return pure_llama3(code + success)
    else:
        print(error)
        execute_code(filter_python(pure_llama3(f"failed to execute {error} while running {code}")))

def img_dealing(user_input):
    response = AIClient.safe_predict(prompt_distiguisher_img + user_input)
    if "img_from_camera" in response:
        capture_photo()
        return dealing.analyze_image_or_video("captured_photo.jpg", user_input)
    elif "img_from_screen" in response:
        take_screenshot()
        return dealing.analyze_image_or_video("screenshot.png", user_input)
    elif "generate_img" in response:
        return dealing.img_generate(user_input, "null")
    else:
        return "from where sir, screen or web cam"

def website_dealing(user_input):
    web_con = webscraper()
    prompt = f"Please respond to the following message considering the context provided: {web_con} query: {user_input}"
    return pure_llama3(prompt)

def screanshare():
    SCREENSHARE()

def live_webcam():
    result = EYE()
    if result == "stop":
        return "close_webcam"

def video_dealing(user_input):
    record_screen()
    return dealing.analyze_image_or_video("output.mp4", user_input)

def pdf_dealing(user_input):
    dealing.pdf_dealer(user_input)

def excel_dealing(user_input):
    dealing.excel_dealer(user_input)

def powerpoint_dealing(user_input):
    response = AIClient.safe_predict(powerpoint_distiguisher_prompt + f" {user_input}")
    if "generate_pptx" in response:
        generate_powerpoint(user_input=user_input)
    else:
        dealing.powerpoint_dealer(user_input)

def chat(user_input):
    return AIClient.llama(user_input)

def application_dev(user_input):
    run_codebrew(user_input)

def web_app(user_input):
    run_codebrew(user_input)

def Operate(user_input):
    logging.info(f"Received user input: {user_input}")
    
    q = prompt_main + user_input
    response = AIClient.safe_predict(q)
    
    logging.info(f"AI response: {response}")
    
    try:
        tags = response.split('+')
        results = []

        for tag in tags:
            tag = tag.strip()
            if "automation" in tag:
                result = automation(user_input)
                speak(result)
                results.append("automation")
            
            elif "realtime-webcam" in tag:
                speak("OK sir, trying to open the webcam")
                result = live_webcam()
                if result == "close_webcam":
                    speak("Closing the webcam")
                    return "close_webcam"
                results.append("realtime-webcam")

            elif "click" in tag:
                text = str(user_input)
                text = text.replace("jarvis", "")
                text = text.replace("click", "")
                text = text.replace("on", "")
                speak("OK sir, trying to click on the button")
                if "double" in text:
                    try:
                        text = text.replace("double", "")
                        from backend.modules.ocr.ocron import ocr_on
                        results.append(ocr_on(text, True))
                    except:
                        text = text.replace("double", "")
                        from backend.modules.ocr.ocroff import ocr_off
                        results.append(ocr_off(text, True)) 
                else:
                    try:
                        text = text.replace("", "")
                        from backend.modules.ocr.ocron import ocr_on
                        results.append(ocr_on(text, True))
                    except:
                        text = text.replace("", "")
                        from backend.modules.ocr.ocroff import ocr_off
                        results.append(ocr_off(text, True)) 

            elif "real-time-knowledge" in tag:
                result = SEARCH(user_input)
                speak(result)
                results.append("real-time-knowledge")
            
            elif "img-dealing" in tag:
                result = img_dealing(user_input)
                speak(result)
                results.append("img-dealing")
            
            elif "website-dealing" in tag:
                result = website_dealing(user_input)
                speak(result)
                results.append("website-dealing")
            
            elif "screenshare" in tag:
                speak("OK sir, trying to share the screen")
                screanshare()
                results.append("screenshare")
            
            elif "video-dealing" in tag:
                speak("OK sir, trying to record the video")
                result = video_dealing(user_input)
                speak(result)
                results.append("video-dealing")
            
            elif "pdf-dealing" in tag:
                speak("OK sir, trying to deal with the pdf")
                pdf_dealing(user_input)
                results.append("pdf-dealing")
            
            elif "excel-dealing" in tag:
                speak("OK sir, trying to deal with the excel")
                excel_dealing(user_input)
                results.append("excel-dealing")
            
            elif "powerpoint-dealing" in tag:
                speak("OK sir, trying to deal with the powerpoint")
                powerpoint_dealing(user_input)
                results.append("powerpoint-dealing")
            
            elif "chat" in tag:
                result = chat(user_input)
                speak(result)
                results.append("chat")
            
            elif "application-dev" in tag:
                speak("OK sir, trying to develop the application")
                application_dev(user_input)
                results.append("application-dev")

            elif "web-app" in tag:
                speak("OK sir, trying to develop the web application")
                web_app(user_input)
                results.append("web-app")

            else:
                logic(user_input)

        return '+'.join(results)

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        speak("Sorry, an error occurred while processing the request.")
        return f"Error: {str(e)}"
