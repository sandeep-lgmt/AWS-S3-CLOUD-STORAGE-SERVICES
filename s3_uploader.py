import boto3
import logging
from botocore.exceptions import NoCredentialsError, EndpointConnectionError
import os
import time
import threading
from datetime import datetime
from PIL import ImageGrab  # For capturing screenshots
from boto3.s3.transfer import TransferConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class S3Uploader:
    def __init__(self):
        try:
            # Initialize S3 client using credentials from %USERPROFILE%\.aws\credentials
            self.s3 = boto3.client('s3')
            self.bucket_name = 'sandeepkumar1'  # Bucket name set to 'sandeepkumar1'
            logging.info("S3 client initialized successfully.")
        except NoCredentialsError:
            logging.error("AWS credentials not found! Ensure they are correctly configured.")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during S3 client initialization: {e}")
            raise

    def upload_to_s3(self, file_path):
        """Upload a file to S3 using chunked uploads and encryption."""
        try:
            # Chunked upload configuration: Max 5 MB per chunk
            config = TransferConfig(multipart_chunksize=5 * 1024 * 1024, multipart_threshold=5 * 1024 * 1024)

            logging.info(f"Uploading {file_path} to bucket {self.bucket_name}...")
            self.s3.upload_file(
                file_path,
                self.bucket_name,
                os.path.basename(file_path),
                ExtraArgs={'ServerSideEncryption': 'AES256'},
                Config=config,
            )
            logging.info(f"Uploaded {file_path} successfully.")
        except NoCredentialsError as e:
            logging.error(f"Credentials issue: {e}")
        except EndpointConnectionError as e:
            logging.warning(f"Endpoint connection error: {e}. Retrying...")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")

def capture_screenshot_and_upload(uploader, interval, temp_dir):
    """Periodically capture screenshots and upload them to S3."""
    while True:
        # Capture the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(temp_dir, f"screenshot_{timestamp}.png")

        # Capture the screenshot
        ImageGrab.grab().save(screenshot_path)
        logging.info(f"Captured screenshot: {screenshot_path}")

        # Upload the screenshot to S3
        uploader.upload_to_s3(screenshot_path)

        # Delete the local file after upload to save space
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            logging.info(f"Deleted local file: {screenshot_path}")

        # Wait for the next interval
        time.sleep(interval)

if __name__ == "__main__":
    # Configuration
    temp_dir = os.path.join(os.getcwd(), "temp")  # Temporary directory for screenshots
    os.makedirs(temp_dir, exist_ok=True)  # Create the directory if it doesn't exist
    interval = 60  # Capture interval in seconds (e.g., 60 seconds)

    # Initialize the S3 uploader
    uploader = S3Uploader()

    # Start the screenshot capture and upload thread
    threading.Thread(target=capture_screenshot_and_upload, args=(uploader, interval, temp_dir), daemon=True).start()

    # Keep the main thread running to prevent the script from exiting
    while True:
        time.sleep(1)