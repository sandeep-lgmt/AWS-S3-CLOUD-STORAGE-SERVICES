from PIL import ImageGrab
import time
import os
import boto3
import requests

class ScreenshotHandler:
    def fetch_config(self):
        response = requests.get(" https://ap-south-1.console.aws.amazon.com/s3/buckets/sandeepkumar1?region=ap-south-1&bucketType=general&tab=objects")

        def __init__(self):
            self.upload_bucket = 'sandeepkumar1'

    # Check if the response was successful
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.text}")
            raise Exception(f"Failed to fetch config: {response.status_code}")
    
        return response.json()


    def capture_screenshot(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"screenshot_{timestamp}.png"
        img = ImageGrab.grab()
        img.save(file_name)
        self.upload_to_s3(file_name)
        os.remove(file_name)  # Clean up after upload

    def upload_to_s3(self, file_name):
        s3 = boto3.client('s3')
        s3.upload_file(file_name, self.upload_bucket, file_name)