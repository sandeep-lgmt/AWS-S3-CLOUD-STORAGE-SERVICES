import boto3

class Uploader:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = 'sandeepkumar1'

    def upload_file(self, file_name):
        self.s3.upload_file(file_name, self.bucket_name, file_name)