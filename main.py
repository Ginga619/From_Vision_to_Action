import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time


import google.generativeai as genai

from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("google_api")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

from PIL import Image

import pygame
import time


def play_mp3(file_path):
    # Initialize the pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(file_path)

    # Play the MP3 file
    pygame.mixer.music.play()
    print("Playing:", file_path)

    # Wait until the playback is finished
    while pygame.mixer.music.get_busy():
        time.sleep(1)

import streamlit as st


st.set_page_config(layout="wide")
st.image("IMG.png")
with st.expander("Getting Started"):
    st.write('''
        1. **Draw**: Use your index finger to draw mathematical expressions.
    2. **Erase**: Combine your thumb and index finger to erase parts of your drawing.
    3. **Clear Canvas**: Use your thumb and pinky fingers together to clear the entire canvas.
    4. **Get Solution**: Open all fingers except your ring finger to submit your math problem and get a solution.


    Refer to the gesture guide below for visual cues.
    ''')
    st.image("Gestures.png")
col1, col2 = st.columns([2, 1])
with col1:
    run = st.checkbox('Run', value=True)
    FRAME_WINDOW = st.image([])
# Initialize session state for persistent variables
if 'canvas' not in st.session_state:
    st.session_state['canvas'] = None  # Canvas for drawing
if 'prev_pos' not in st.session_state:
    st.session_state['prev_pos'] = None  # Previous drawing position
if 'draw_color' not in st.session_state:
    st.session_state['draw_color'] = (255, 0, 0)  # Default color: Blue
if 'output_text' not in st.session_state:
    st.session_state['output_text'] = ""  # To store AI response

# Streamlit UI for color selection
with col2:
    st.subheader("Choose Drawing Color")
    selected_color = st.radio(
        "Select a color:",
        options=["Blue", "Red", "Green", "Yellow"],
        index=0
    )
    # Placeholder for AI response
    output_text_area = st.title("Answer")
    output_text_area = st.empty()




# Map color names to BGR values
color_map = {
    "Blue": (225, 153, 153),
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Yellow": (0, 255, 255)
}

# Update draw color in session state
st.session_state['draw_color'] = color_map[selected_color]


# Initialize the webcam to capture video
# The '2' indicates the third camera connected to your computer; '0' would usually refer to the built-in camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.9, minTrackCon=0.5)


def getHandInfo(img):
    # Find hands in the current frame
    # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
    # The 'flipType' parameter flips the image, making it easier for some detections
    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Check if any hands are detected
    if hands:
        # Information for the first hand detected
        hand = hands[0]  # Get the first hand detected
        lmList = hand["lmList"]  # List of 21 landmarks for the first hand
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    else:
        return None


def draw(info, erase_radius=20):
    fingers, lmlist = info
    current_pos = None
    canvas = st.session_state['canvas']

    # Drawing with index finger
    if fingers == [0, 1, 0, 0, 0]:  # Index finger up
        current_pos = lmlist[8][0:2]
        if st.session_state['prev_pos'] is None:
            st.session_state['prev_pos'] = current_pos
        # Draw a line on the canvas
        cv2.line(canvas, st.session_state['prev_pos'], current_pos, st.session_state['draw_color'], 10)
        # Visualize the drawing circle
        cv2.circle(img, current_pos, 10, st.session_state['draw_color'], -1)  # Filled circle at the fingertip

    # Erasing with thumb and index finger
    elif fingers == [1, 1, 0, 0, 0]:  # Thumb and index finger up
        erase_pos = lmlist[8][0:2]  # Index finger tip position
        # Erase from the canvas
        cv2.circle(canvas, erase_pos, erase_radius, (0, 0, 0), -1)  # Black circle for erasing in canvas
        # Visualize the eraser circle
        cv2.circle(img, erase_pos, erase_radius, (225, 225, 225), -1)  # White eraser on camera

    # Clearing canvas with thumb and pinky
    elif fingers == [1, 0, 0, 0, 1]:
        canvas = np.zeros_like(canvas) # Thumb and pinky up
        st.session_state['canvas'] = np.zeros_like(canvas)

    # Return current position for smooth drawing
    st.session_state['prev_pos'] = current_pos
    return canvas




def send_to_ai(canvas, fingers):
    if fingers == [1, 1, 1, 0, 1]:  # Specific gesture to trigger AI
        pil_image = Image.fromarray(canvas)

        with st.spinner():
            response = model.generate_content(["Solve this Math Problem", pil_image])
            time.sleep(3)  # Simulate API delay

        play_mp3("beep2.mp3")
        print(fingers)
        print(response.text)


        return response.text

prev_pos = None
canvas = None
image_combined = None
output_text = ""


while run == True:
    success, img = cap.read()
    img = cv2.flip(img, flipCode=1)

    # Initialize canvas if not already done
    if st.session_state['canvas'] is None:
        st.session_state['canvas'] = np.zeros_like(img)

    # Get hand information
    info = getHandInfo(img)
    if info:
        fingers, lmlist = info
        st.session_state['canvas'] = draw(info)

        # Send canvas to AI if the specific gesture is detected
        response_text = send_to_ai(st.session_state['canvas'], fingers)
        if response_text:
            st.session_state['output_text'] = response_text

    # Update AI response in Streamlit UI
    output_text_area.text(st.session_state['output_text'])

    # Combine original frame and canvas
    image_combined = cv2.addWeighted(img, 0.7, st.session_state['canvas'], 0.3, 0)
    FRAME_WINDOW.image(image_combined, channels="BGR")

    cv2.waitKey(1)
else:
    st.write("Toggle 'Run' to start processing.")
