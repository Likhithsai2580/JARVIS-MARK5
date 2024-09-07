import cv2
import base64
from groq import Groq
import os

API = os.getenv("GROQ_API")
def capture_and_recognize_image():
    """Captures an image from the webcam, encodes it, and sends it for recognition using the Groq API."""
    
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
    
    # Release webcam after capturing the image
    cap.release()
    cv2.destroyAllWindows()

    # Save the image temporarily (optional step)
    temp_img_filename = 'captured_image.jpg'
    with open(temp_img_filename, 'wb') as f:
        f.write(base64.b64decode(jpg_as_text))
    
    # Perform image recognition using the Groq API
    try:
        # Initialize the Groq client
        client = Groq(api_key=api)

        # Send the image for recognition (replace with actual hosting URL if needed)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"file://{temp_img_filename}",  # Using local file path
                            },
                        },
                    ],
                }
            ],
            model="llava-v1.5-7b-4096-preview",
        )

        # Output the recognition result
        print("Recognition Result:", chat_completion.choices[0].message.content)

    except Exception as e:
        print(f"Error during image recognition: {e}")

# Capture the image and perform recognition
capture_and_recognize_image()
