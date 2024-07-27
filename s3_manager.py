import os
import boto3
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Get credentials from environment variables
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Initialize S3 client
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY) if ACCESS_KEY and SECRET_KEY else None

def upload_to_s3(local_path, bucket_name, s3_path):
    if os.path.isdir(local_path):
        for item in os.listdir(local_path):
            full_path = os.path.join(local_path, item)
            s3_item_path = os.path.join(s3_path, item).replace("\\", "/")
            upload_to_s3(full_path, bucket_name, s3_item_path)
    else:
        s3.upload_file(local_path, bucket_name, s3_path)
        print(f"Uploaded {local_path} to {bucket_name}/{s3_path}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_buckets', methods=['GET'])
def fetch_buckets():
    if not s3:
        return jsonify({'error': 'S3 client not initialized. Check your AWS credentials.'}), 500
    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return jsonify(buckets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    if not s3:
        return jsonify({'error': 'S3 client not initialized. Check your AWS credentials.'}), 500
    if 'folder' not in request.files:
        return jsonify({'error': 'No folder part'}), 400
    files = request.files.getlist('folder')
    bucket_name = request.form.get('bucket')
    if not bucket_name:
        return jsonify({'error': 'No bucket selected'}), 400

    try:
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            s3_path = os.path.join('python', filename).replace("\\", "/")
            upload_to_s3(file_path, bucket_name, s3_path)
            os.remove(file_path)
        return jsonify({'message': 'Upload completed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list_bucket_contents', methods=['GET'])
def list_bucket_contents():
    if not s3:
        return jsonify({'error': 'S3 client not initialized. Check your AWS credentials.'}), 500
    bucket_name = request.args.get('bucket')
    if not bucket_name:
        return jsonify({'error': 'No bucket selected'}), 400

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        contents = [obj['Key'] for obj in response.get('Contents', [])]
        return jsonify(contents)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_bucket', methods=['POST'])
def clear_bucket():
    if not s3:
        return jsonify({'error': 'S3 client not initialized. Check your AWS credentials.'}), 500
    bucket_name = request.json.get('bucket')
    if not bucket_name:
        return jsonify({'error': 'No bucket selected'}), 400

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        return jsonify({'message': 'All objects deleted from the bucket'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_item', methods=['POST'])
def delete_item():
    if not s3:
        return jsonify({'error': 'S3 client not initialized. Check your AWS credentials.'}), 500
    bucket_name = request.json.get('bucket')
    key = request.json.get('key')
    if not bucket_name or not key:
        return jsonify({'error': 'Bucket or key not provided'}), 400

    try:
        s3.delete_object(Bucket=bucket_name, Key=key)
        return jsonify({'message': f"Deleted '{key}' from the bucket"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not s3:
        print("Warning: S3 client not initialized. Check your AWS credentials.")
    app.run(host='0.0.0.0', port=5000, debug=True)
