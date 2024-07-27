```markdown
# S3 Folder Uploader

## Table Of Contents
- [Overview](#overview)
  - [Key Features](#key-features)
  - [User Interface](#user-interface)
  - [How to Use](#how-to-use)
  - [Technical Summary](#technical-summary)
- [Prerequisites](#prerequisites)
  - [Example `secrets.py`](#example-secretspy)
  - [Directory Structure](#directory-structure)
  - [Running the Script](#running-the-script)
  - [Additional Notes](#additional-notes)

## Overview

The S3 Folder Uploader is a graphical user interface (GUI) application built using Tkinter and Boto3 that allows users to interact with their Amazon S3 buckets. The application enables users to upload folders, list bucket contents, clear buckets, and delete specific items from a bucket, all through a user-friendly dark-themed interface.

### Key Features

1. **Browse and Select Local Folders**:
   - Users can browse and select a local folder to upload to an S3 bucket.

2. **Fetch and Select S3 Buckets**:
   - The application fetches the list of available S3 buckets, allowing users to select the target bucket for operations.

3. **Upload Folders to S3**:
   - The selected local folder and its contents are uploaded to the specified S3 bucket, maintaining the folder structure.

4. **List Bucket Contents**:
   - Users can list all files and folders currently in the selected S3 bucket.

5. **Clear Bucket**:
   - This feature allows users to delete all contents of the selected S3 bucket.

6. **Delete Specific Items**:
   - Users can select and delete specific files or folders from the S3 bucket.

### User Interface

- **Dark Theme**: The application features a modern dark theme for a sleek and visually appealing interface.
- **Interactive Widgets**: The application uses `ttk` (Themed Tkinter) widgets for a consistent look and feel.
- **Buttons and Listboxes**: Buttons for various actions (upload, fetch, list, clear, delete) and listboxes to display bucket contents.

### How to Use

1. **Select a Folder**:
   - Click the "Browse" button to select a local folder.

2. **Fetch Buckets**:
   - Click the "Fetch Buckets" button to load the list of available S3 buckets.

3. **Select a Bucket**:
   - Choose the desired S3 bucket from the dropdown menu.

4. **Upload Folder**:
   - Click the "Upload" button to upload the selected folder to the chosen S3 bucket.

5. **List Bucket Contents**:
   - Click the "List Contents" button to display the contents of the selected bucket.

6. **Clear Bucket**:
   - Click the "Clear Bucket" button to delete all contents of the selected bucket. A confirmation dialog ensures this action is intentional.

7. **Delete Selected Item**:
   - Select an item from the list and click the "Delete Selected" button to remove it from the bucket. A confirmation dialog ensures this action is intentional.

### Technical Summary

- **Language**: Python
- **Libraries**: Tkinter for GUI, Boto3 for AWS S3 interaction
- **Design**: Dark-themed interface using `ttk.Style` for consistency and modern look

This application simplifies the management of S3 buckets by providing a graphical interface for common tasks, making it accessible to users who prefer not to use command-line tools or AWS Management Console.

## Prerequisites

To run the S3 Folder Uploader script, you need to ensure the following prerequisites are met:

1. **Python Installation**:
   - Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/).

2. **Required Python Packages**:
   - **Tkinter**: This is included with standard Python installations. If you're using a minimal installation, you might need to install it separately.
   - **Boto3**: This package is required to interact with AWS S3. You can install it using pip:
     ```bash
     pip install boto3
     ```

3. **AWS Credentials**:
   - You need AWS credentials (`ACCESS_KEY` and `SECRET_KEY`) to authenticate and interact with your S3 buckets. These should be stored in a `secrets.py` file in the same directory as the script, with the following format:
     ```python
     ACCESS_KEY = 'your_access_key_here'
     SECRET_KEY = 'your_secret_key_here'
     ```

4. **AWS Permissions**:
   - Ensure that the AWS credentials used have sufficient permissions to list, upload, and delete objects in the S3 buckets.

### Example `secrets.py`

```python
ACCESS_KEY = 'your_access_key_here'
SECRET_KEY = 'your_secret_key_here'
```

### Directory Structure

Ensure your script and `secrets.py` are in the same directory:

```
project_directory/
├── s3_folder_uploader.py
└── secrets.py
```

### Running the Script

1. Navigate to the directory containing the script.
2. Run the script using Python:
   ```bash
   python s3_folder_uploader.py
   ```

### Additional Notes

- **AWS Configuration**: If you prefer not to hardcode the credentials in the `secrets.py` file, you can configure your AWS credentials using the AWS CLI. This will store your credentials in the `~/.aws/credentials` file, which Boto3 can use automatically.
  ```bash
  aws configure
  ```

- **Error Handling**: Ensure that you handle any potential errors such as invalid credentials, network issues, or permission errors.

By following these prerequisites, you should be able to successfully run the S3 Folder Uploader script and interact with your S3 buckets through the provided GUI.
```

This README provides a comprehensive guide on how to use the S3 Folder Uploader application, including an overview of its features, prerequisites, setup instructions, and how to run the script.