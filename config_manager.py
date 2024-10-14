import boto3
from botocore.exceptions import NoCredentialsError
import requests

class ConfigManager:
    def __init__(self):
        self.config = self.fetch_config()

    def fetch_config(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        try:
            url = s3.generate_presigned_url('get_object',
                                              Params={'Bucket': 'laddibucket', 'Key': 'config.json'},
                                              ExpiresIn=3600)
            response = requests.get(url)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch config: {response.status_code} - {response.text}")

            return response.json()

        except NoCredentialsError:
            raise Exception("Credentials not available")