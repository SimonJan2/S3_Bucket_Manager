from secrets_1 import ACCESS_KEY, SECRET_KEY
from boto3 import client
import os

# Initialize the S3 client
s3 = client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Define the folder path
folder_path = 'D:\\DevSecOps\\Python\\Project'

# Function to recursively upload files and folders
def upload_to_s3(local_path, bucket_name, s3_path):
    if os.path.isdir(local_path):
        for item in os.listdir(local_path):
            full_path = os.path.join(local_path, item)
            s3_item_path = os.path.join(s3_path, item).replace("\\", "/")
            upload_to_s3(full_path, bucket_name, s3_item_path)
    else:
        s3.upload_file(local_path, bucket_name, s3_path)
        print(f"Uploaded {local_path} to {bucket_name}/{s3_path}")

# Start the upload process
upload_to_s3(folder_path, 'backup-simon-test', 'python')
print("Upload completed.")
