#https://colab.research.google.com/drive/1xenMnAqGydJnsNV5C9aQ4ysrOCdNgXdf?usp=sharing

import cv2
import requests
import json
import time
import base64

cache = {}

def get_url():
    """Fetches the camera URL from the configuration file and caches it."""
    try:
        # Check if URL exists in cache and is not expired
        if 'url' in cache and cache['url'][1] > time.time():
            return cache['url'][0]
        
        with open('config/config.json') as config_file:
            config = json.load(config_file)
            url = config.get('OBJ_DETECTION_URL')
            if url is None:
                raise ValueError("camera URL not found in config file")
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

def capture_and_send_image():
    """Captures an image from the webcam, encodes it, and sends it to the server."""
    api_url = get_url()
    
    if api_url is None:
        print("No API URL available.")
        return
    
    # Replace this URL with your ngrok URL or endpoint
    ngrok_url = f"{api_url}/stream"

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        cap.release()
        return

    # Encode frame to JPEG
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    # Send frame to server
    try:
        response = requests.post(ngrok_url, data={'image': jpg_as_text})
        if response.status_code == 200:
            print("Frame sent successfully")
        else:
            print(f"Failed to send frame: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
