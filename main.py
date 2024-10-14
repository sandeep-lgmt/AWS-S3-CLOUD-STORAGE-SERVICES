import time
import logging
import os
import atexit
from config_manager import ConfigManager
from activity_tracker import ActivityTracker
from screenshot_manager import ScreenshotManager
from s3_uploader import S3Uploader
from timezone_handler import TimezoneHandler
from utils import check_single_instance, detect_battery_level

logging.basicConfig(level=logging.INFO, filename='agent.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

pid_file = "agent.pid"

def remove_pid_file():
    if os.path.exists(pid_file):
        os.remove(pid_file)

atexit.register(remove_pid_file)

def main():
    check_single_instance()

    config = ConfigManager()
    tracker = ActivityTracker()
    screenshot_mgr = ScreenshotManager(config)
    uploader = S3Uploader()
    timezone_handler = TimezoneHandler()
    
    try:
        while True:
            if detect_battery_level() < 20:
                logging.warning("Low battery detected. Suspending tracking.")
                time.sleep(60)  # Pause for 1 minute before rechecking
                continue

            if tracker.detect_genuine_activity():
                screenshot_mgr.capture_and_queue()

            uploader.retry_failed_uploads()
            timezone_handler.handle_timezone_change()

            time.sleep(config.get_interval())

    except KeyboardInterrupt:
        logging.info("Shutting down safely...")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()