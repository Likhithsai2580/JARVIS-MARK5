from PIL import ImageGrab
import io
from time import sleep, time as t
import requests
import pyautogui as pag
import time
import json
cache = {}
C = t()

def get_url():
    """Fetches the camera URL from the configuration file and caches it."""
    try:
        # Check if URL exists in cache and is not expired
        if 'url' in cache and cache['url'][1] > time.time():
            return cache['url'][0]
        
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            url = config.get('OCR_LINK')
            if url is None:
                raise ValueError("OCR_LINK URL not found in config file")
            # Cache the URL with expiration time of 1 hour
            cache['url'] = (url, time.time() + 3600)
            return url
    except FileNotFoundError:
        print("Config file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON in config file.")
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None

def ocr_on(search_string, double_click=False):
    url = get_url()
    screenshot = ImageGrab.grab()
    image_bytes = io.BytesIO()
    screenshot.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    if double_click:
        payload = {
            "search_string": search_string,
            "double_click": "on"
        }
    else:
        payload = {
            "search_string": search_string,
            "double_click": "off"
        }
    
    files = {'image': image_bytes}

    r = requests.post(url, files=files, data=payload)
    if "error" in r:
        return f"no button found named {search_string}"
    else:
        screenshot.close()
        print(t() - C)
        response = r.json()
        print(response["time"])
        point = response["point"]
        if double_click:
            pag.click(point)
            sleep(0.30)
            pag.click(point)
        else:
            pag.click(point)