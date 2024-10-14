# AWS-S3-CLOUD-STORAGE-SERVICES

Employee Activity Tracker – Desktop Agent
This project provides a Python-based desktop agent application to monitor employee activity, capture screenshots, and upload them to Amazon S3 or similar cloud storage. It includes robust features like error handling, auto-update mechanism, network failure management, firewall detection, and low battery detection.

Table of Contents
Features
Prerequisites
Installation
Configuration
How to Run
Error Handling and Resilience
Optional Features
Project Structure
Tests
Troubleshooting
License
Features
Activity Tracking

Monitors user input (keyboard, mouse) and detects genuine activity.
Differentiates between real activity and script-based emulation.
Screenshot Management

Configurable screenshot intervals and blurred/unblurred screenshots.
Stores screenshots locally during connection issues and uploads them later.
Time Zone Management

Automatically adjusts timestamps based on system time zone changes.
Error Handling and Resilience

Detects network disconnections, queues uploads, and retries automatically.
Handles abrupt disconnections and maintains data integrity.
Detects firewall restrictions and provides user-friendly notifications.
Optional Features

Auto-update mechanism to download and install updates seamlessly.
Battery level detection to pause activity tracking on low battery.
MFA-based authentication for enhanced security.
Prerequisites
Python 3.8+ installed.
AWS credentials configured using either:
~/.aws/credentials:
ini
Copy code
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
IAM Role if the application runs in an AWS-hosted environment.
AWS S3 bucket to store screenshots and logs.
PIP package manager.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/employee-tracker.git
cd employee-tracker
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Configuration
Modify the config endpoint URL in config_manager.py to point to your web application:

python
Copy code
response = requests.get("<your_config_endpoint>")
The configuration should include:

json
Copy code
{
  "interval": 300,
  "blur": true
}
interval: Time (in seconds) between consecutive screenshots.
blur: Set to true or false to enable/disable blurred screenshots.
How to Run
Start the application:

bash
Copy code
python main.py
Run tests:

bash
Copy code
pytest tests/
Stop the application safely with Ctrl + C.

Error Handling and Resilience
The application is designed to handle the following scenarios gracefully:

Network Issues:

No Internet Connection:
Uploads are queued locally and retried when the connection is restored.
Firewall Restrictions:
Detects blocked connections and logs an error message.
Abrupt Disconnection:

Data is saved locally during shutdown, preventing data loss.
Battery Management:

Detects low battery levels and suspends tracking to save power.
Optional Features
Auto-Update Mechanism
Install PyUpdater:
bash
Copy code
pip install pyupdater
Use this code snippet in main.py to enable updates:
python
Copy code
from pyupdater.client import Client

def check_for_updates():
    client = Client("<your_client_config>", refresh=True)
    update = client.update_check("<your_app_name>", "<your_version>")
    if update:
        update.download()
        update.extract_restart()
MFA Authentication using AWS Cognito
Enable multi-factor authentication for configuration changes:

python
Copy code
import boto3

def authenticate_with_mfa(username, password, mfa_code):
    client = boto3.client('cognito-idp')
    response = client.admin_initiate_auth(
        UserPoolId='<your_user_pool_id>',
        ClientId='<your_client_id>',
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password,
            'SMS_MFA_CODE': mfa_code
        }
    )
    return response
Project Structure
bash
Copy code
employee_tracker/
│
├── main.py               # Entry point of the application
├── config_manager.py     # Handles configuration updates from the web app
├── activity_tracker.py   # Monitors and captures user activity
├── screenshot_manager.py # Handles screenshot capturing and uploads
├── s3_uploader.py        # Uploads files to S3 with retry logic
├── timezone_handler.py   # Manages time zone changes
├── utils.py              # Utility functions (battery, instance check)
├── tests/                # Unit and integration tests
│   ├── test_activity.py  # Unit test for activity tracking
│   ├── test_upload.py    # Test for S3 upload functionality
│   └── test_config.py    # Test for config updates
├── requirements.txt      # List of dependencies
└── README.md             # Documentation (this file)
Tests
Run all tests:
bash
Copy code
pytest tests/
Example Test Case: tests/test_upload.py:
python
Copy code
import unittest
from s3_uploader import S3Uploader

class TestS3Uploader(unittest.TestCase):
    def test_upload_to_s3(self):
        uploader = S3Uploader()
        # Mock S3 interaction or use a test bucket
        self.assertIsNone(uploader.upload_to_s3("test.png", "test-bucket"))

if __name__ == "__main__":
    unittest.main()
Troubleshooting
Problem: Multiple instances are running.
Solution: Ensure only one instance by calling check_single_instance() in utils.py.

Problem: Uploads are failing due to network issues.
Solution: Verify that the Internet connection is available and firewall rules allow outbound requests.

Problem: Screenshots are not being captured.
Solution: Ensure Pillow and opencv-python-headless are installed.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a pull request.
Acknowledgments
Boto3 for seamless AWS integration.
PyAutoGUI and Pillow for screenshot capture.
PyUpdater for automatic updates.
This README.md provides everything needed to install, configure, run, and troubleshoot the Employee Activity Tracker application. Adjust configurations as required to fit your environment and infrastructure.






