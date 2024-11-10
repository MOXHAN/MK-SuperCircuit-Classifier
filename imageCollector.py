import cv2
import numpy as np
from mss import mss
import keyboard
import os
from datetime import datetime
import time

def capture_screen(monitor):
    with mss() as sct:
        screenshot = np.array(sct.grab(monitor))
        return cv2.cvtColor(screenshot, cv2.COLOR_RGBA2RGB)

def save_screenshot(screen, key_pressed, output_dir="game_captures"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if key_pressed == "x":
        key_pressed = "forward"
    
    # Generate filename with timestamp and key pressed
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{timestamp}_{key_pressed}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    # Save the image
    cv2.imwrite(filepath, screen)
    print(f"Captured screenshot with {key_pressed} press: {filename}")

def main():
    
    # Get lower-half of screen
    monitor = {
        "top": 540,    # Half of 1080
        "left": 0,
        "width": 1920,
        "height": 500,  # Adjusted to skip the taskbar
    }

    arrow_keys = ['up', 'down', 'left', 'right',"x"]

    print("Screen capture started. Press 'esc' to exit.")
    
    while True:
        if keyboard.is_pressed('esc'):
            print("Exiting...")
            break
            
        for key in arrow_keys:
            # Check if key is currently pressed
            if keyboard.is_pressed(key):
                # Only capture if this is a new press (not held down)
                #if not key_states[key]:
                screen = capture_screen(monitor)
                save_screenshot(screen, key)

                # This breaks the for-loop once a key from the list is pressed
                # This is necessary so that the arrow-keys are prioritized over the "x"-key
                break

        # Small sleep to prevent high CPU usage
        time.sleep(0.25)

if __name__ == "__main__":
    main()