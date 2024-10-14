import os
from PIL import ImageGrab
import cv2
import time
from s3_uploader import S3Uploader
import logging 

class ScreenshotManager:
    def __init__(self, config):
        self.config = config
        self.uploader = S3Uploader()
        self.queue = []  # Queue to store screenshots during disconnection

    def capture_screenshot(self, blur=False):
        screenshot = ImageGrab.grab()
        if blur:
            screenshot = cv2.GaussianBlur(screenshot, (21, 21), 0)
        filename = f"screenshot_{int(time.time())}.png"
        screenshot.save(filename, "PNG")
        return filename

    def capture_and_queue(self):
        blur = self.config.is_blur_enabled()
        screenshot_path = self.capture_screenshot(blur)
        self.queue.append(screenshot_path)
        self.upload_queue()

    def upload_queue(self):
        for screenshot in self.queue[:]:
            try:
                self.uploader.upload_to_s3(screenshot, "sandeepkumar1")
                os.remove(screenshot)
                self.queue.remove(screenshot)
            except Exception as e:
                logging.warning(f"Failed to upload {screenshot}: {e}")
                break  # Avoid emptying the queue if upload fails