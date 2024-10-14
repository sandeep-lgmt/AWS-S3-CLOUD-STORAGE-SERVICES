import pyautogui
import time

class ActivityTracker:
    def __init__(self):
        self.last_position = pyautogui.position()

    def detect_genuine_activity(self):
        current_position = pyautogui.position()
        if current_position != self.last_position:
            self.last_position = current_position
            return True
        return False