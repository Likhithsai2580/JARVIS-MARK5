from backend.modules.search import SEARCH
from backend.modules.llms import AIClient, pure_llama3
from filter import filter_python, filter_json
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

def get_os_info():
    # Get the OS name
    os_name = platform.system()
    
    # Get the OS version
    os_version = platform.version()
    
    # Get the OS release
    os_release = platform.release()
    
    return os_name+os_version+os_release

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

extension_prompt = """
"""

prompt_main = """
Given the user query, identify and respond with the relevant tags from the following list: [automation, real-time-knowledge, img-dealing, website-dealing, screanshare, video-dealing, pdf-dealing, excel-dealing, powerpoint-dealing, chat, application-dev, web-app, click]. If the query involves multiple tasks, combine the appropriate tags with a plus sign. Respond with only the tags and nothing else.
Examples:
Query: "Read the selected PDF and summarize it."
Response: pdf-dealing+automation

Query: "i want to share the screen"
Response": sharescreen

Query: "open youtube"
Response: automation

Query: "make a portfolio"
Response: website-dealing

Query: "who won elections"
Response: real-time-knowledge

Query: "download video from website"
Response: website-dealing

Query: "study this video"
Response: video-dealing
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
"""+get_os_info()

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
def run_codebrew(user_input):
    # Initialize the LLM instance with the desired configurations
    llm = LLM(
        verbose=True, 
        max_tokens=4096, 
        messages=samplePrompt(), 
        system_prompt=codebrewPrompt()
    )
    
    # Create an instance of CodeBrew with the initialized LLM
    codebrew = CodeBrew(llm, keepHistory=True)
    
    # Start the conversation loop
    while True:
        user_input = input(">>> ")
        response = codebrew.run(user_input)
        print(response)


def record_screen(video_filename='output.mp4', duration=20):
    # Define the codec and create VideoWriter object for MP4
    codec = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4 files
    screen_size = pyautogui.size()  # Get the screen size
    fps = 20  # Frames per second
    out = cv2.VideoWriter(video_filename, codec, fps, screen_size)

    print(f"Recording started. Will record for {duration} seconds...")
    
    start_time = time.time()
    while True:
        # Capture the screen
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Write the frame into the video
        out.write(frame)
        
        # Check if the duration has elapsed
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

    # Release the VideoWriter object
    out.release()
    cv2.destroyAllWindows()
    print(f"Recording completed. Video saved as {video_filename}")

def copy_url_from_browser():
    # Simulate pressing Ctrl+L to focus the address bar
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.5)  # Wait for the focus to shift

    # Simulate pressing Ctrl+C to copy the URL
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Wait for the URL to be copied to the clipboard

def get_url_from_clipboard():
    try:
        # Get URL from clipboard
        url = pyperclip.paste()
        
        # Validate if the clipboard content seems like a URL
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
        # Send an HTTP request to the specified URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Convert the parsed HTML content to a string
            web = soup.prettify()
            
            return web
        else:
            # Handle failed request
            print(f"Failed to retrieve content. Status code: {response.status_code}")
            return None
    
    except requests.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
        return None

def webscraper():
    # Step 1: Copy URL from browser
    copy_url_from_browser()
    
    # Step 2: Get URL from clipboard
    url = get_url_from_clipboard()
    
    if url:
        # Step 3: Scrape the website
        web_content = scrape_website(url)
        
        if web_content:
            print("Web content successfully retrieved and stored in 'web' variable.")
            return web_content
            # Do something with 'web_content'
        else:
            return("Failed to retrieve web content.")
    else:
        return("No valid URL found in clipboard.")

def take_screenshot():
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot to a file
    screenshot.save('screenshot.png')
    
    print("Screenshot saved as 'screenshot.png'.")

def capture_photo():
    # Open a connection to the webcam (usually the first webcam is index 0)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    # Capture a single frame
    ret, frame = cap.read()

    # Release the webcam
    cap.release()
    
    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture image.")
        return

    # Save the captured image
    cv2.imwrite('captured_photo.jpg', frame)
    
    print("Photo saved as 'captured_photo.jpg'.")

def execute_code(code_str):
    success = None
    error = None
    
    try:
        # Create a dictionary to act as the local namespace for exec
        local_namespace = {}
        exec(code_str, {}, local_namespace)
        
        # If exec() succeeds, we store the local namespace in success
        success = local_namespace
    except Exception as e:
        # If an exception occurs, store the exception in error
        error = str(e)
    
    return success, error

def automation(user_input):
    prompt = automation_prompt+user_input
    code = filter_python(pure_llama3(prompt))
    success,error = execute_code(code)
    if success:
        return pure_llama3(code + success)
    else:
        print(error)
        execute_code(filter_python(pure_llama3(f"failed to execute {error} while running {code}")))

def img_dealing(user_input):
    response = AIClient.safe_predict(prompt_distiguisher_img+user_input)
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
    prompt=f"Please respond to the following message considering the context provided: {web_con} query: {user_input}"
    return pure_llama3(prompt)

def screanshare():
    SCREENSHARE()

def live_webcam():
    EYE()

def video_dealing(user_input):
    record_screen()
    return dealing.analyze_image_or_video("output.mp4", user_input)

def pdf_dealing(user_input):
    dealing.pdf_dealer(user_input)

def excel_dealing(user_input):
    dealing.excel_dealer(user_input)

def powerpoint_dealing(user_input):
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
        if "automation" in response:
            automation(user_input)

        elif "click" in response:
            text = str(user_input)
            text = text.replace("jarvis", "")
            text = text.replace("click", "")
            text = text.replace("on", "")
            if "double" in text:
                try:
                    text = text.replace("double","")
                    from backend.modules.ocr.ocron import ocr_on
                    return ocr_on(text, True)
                except:
                    text = text.replace("double","")
                    from backend.modules.ocr.ocroff import ocr_off
                    return ocr_off(text, True) 
            else:
                try:
                    text = text.replace("","")
                    from backend.modules.ocr.ocron import ocr_on
                    return ocr_on(text, True)
                except:
                    text = text.replace("","")
                    from backend.modules.ocr.ocroff import ocr_off
                    return ocr_off(text, True) 
        elif "real-time-knowledge" in response:
            SEARCH(user_input)
        
        elif "img-dealing" in response:
            img_dealing(user_input)
        
        elif "website-dealing" in response:
            website_dealing(user_input)
        
        elif "screenshare" in response:
            screanshare()
        
        elif "video-dealing" in response:
            video_dealing(user_input)
        
        elif "pdf-dealing" in response:
            pdf_dealing(user_input)
        
        elif "excel-dealing" in response:
            excel_dealing(user_input)
        
        elif "powerpoint-dealing" in response:
            powerpoint_dealing(user_input)
        
        elif "chat" in response:
            chat(user_input)
        
        elif "application-dev" in response:
            application_dev(user_input)
        
        elif "web-app" in response:
            web_app(user_input)
        
        else:
            logging.warning(f"Unhandled response: {response}")
            return "Sorry, I don't understand the request."
    except Exception as e:
        return "Sorry, a error occurred while processing the request."