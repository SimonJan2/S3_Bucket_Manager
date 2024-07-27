import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from secrets_1 import ACCESS_KEY, SECRET_KEY
from boto3 import client
import os

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Initialize the S3 client
s3 = client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

def upload_to_s3(local_path, bucket_name, s3_path):
    if os.path.isdir(local_path):
        for item in os.listdir(local_path):
            full_path = os.path.join(local_path, item)
            s3_item_path = os.path.join(s3_path, item).replace("\\", "/")
            upload_to_s3(full_path, bucket_name, s3_item_path)
    else:
        s3.upload_file(local_path, bucket_name, s3_path)
        print(f"Uploaded {local_path} to {bucket_name}/{s3_path}")

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)

def fetch_buckets():
    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        bucket_var.set("")
        bucket_menu['menu'].delete(0, 'end')
        for bucket in buckets:
            bucket_menu['menu'].add_command(label=bucket, command=tk._setit(bucket_var, bucket))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fetching buckets: {e}")

def upload_folder():
    folder_path = folder_path_var.get()
    if not folder_path:
        messagebox.showerror("Error", "Please select a folder to upload.")
        return
    
    bucket_name = bucket_var.get()
    if not bucket_name:
        messagebox.showerror("Error", "Please select an S3 bucket.")
        return

    try:
        upload_to_s3(folder_path, bucket_name, 'python')
        messagebox.showinfo("Success", "Upload completed.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_bucket():
    bucket_name = bucket_var.get()
    if not bucket_name:
        messagebox.showerror("Error", "Please select an S3 bucket.")
        return

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete all contents of the bucket '{bucket_name}'?")
    if confirm:
        try:
            response = s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                    print(f"Deleted {obj['Key']} from {bucket_name}")
            messagebox.showinfo("Success", "All objects deleted from the bucket.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def list_bucket_contents():
    bucket_name = bucket_var.get()
    if not bucket_name:
        messagebox.showerror("Error", "Please select an S3 bucket.")
        return

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            file_list.delete(0, tk.END)
            for obj in response['Contents']:
                file_list.insert(tk.END, obj['Key'])
        else:
            file_list.delete(0, tk.END)
            messagebox.showinfo("Info", "Bucket is empty.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def delete_selected_item():
    bucket_name = bucket_var.get()
    if not bucket_name:
        messagebox.showerror("Error", "Please select an S3 bucket.")
        return

    selected = file_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select an item to delete.")
        return

    key = file_list.get(selected[0])
    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{key}' from the bucket '{bucket_name}'?")
    if confirm:
        try:
            s3.delete_object(Bucket=bucket_name, Key=key)
            file_list.delete(selected[0])
            messagebox.showinfo("Success", f"Deleted '{key}' from the bucket.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Simon Jan - S3 Bucket Manager")
# Set the background color of the window
root.configure(bg="#2e2e2e")

# Apply a style
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#444444", foreground="black")
style.configure("TLabel", padding=6, background="#2e2e2e", foreground="#d3d3d3")
style.configure("TEntry", padding=6, background="#3e3e3e", foreground="#d3d3d3", fieldbackground="#3e3e3e")
style.configure("TListbox", padding=6, background="#3e3e3e", foreground="#d3d3d3")

# Create and set the variables
folder_path_var = tk.StringVar()
bucket_var = tk.StringVar()

# Create the GUI elements
folder_label = ttk.Label(root, text="Folder Path:")
folder_entry = ttk.Entry(root, textvariable=folder_path_var, width=50)
folder_button = ttk.Button(root, text="Browse", command=select_folder)

bucket_label = ttk.Label(root, text="S3 Bucket:")
bucket_menu = ttk.OptionMenu(root, bucket_var, '')

fetch_button = ttk.Button(root, text="Fetch Buckets", command=fetch_buckets)
list_button = ttk.Button(root, text="List Contents", command=list_bucket_contents)
clear_button = ttk.Button(root, text="Clear Bucket", command=clear_bucket, style="Red.TButton")
upload_button = ttk.Button(root, text="Upload", command=upload_folder)

file_list = tk.Listbox(root, width=80, height=20, bg="#3e3e3e", fg="#d3d3d3", selectbackground="#555555", selectforeground="white")
delete_button = ttk.Button(root, text="Delete Selected", command=delete_selected_item, style="Red.TButton")

# Add red style for specific buttons
style.configure("Red.TButton", background="#ff4d4d", foreground="black")

# Layout the GUI elements with padding
folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
folder_entry.grid(row=0, column=1, padx=10, pady=10)
folder_button.grid(row=0, column=2, padx=10, pady=10)

bucket_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
bucket_menu.grid(row=1, column=1, padx=10, pady=10)
fetch_button.grid(row=1, column=2, padx=10, pady=10)

list_button.grid(row=2, column=0, padx=10, pady=10)
clear_button.grid(row=2, column=1, padx=10, pady=10)
upload_button.grid(row=2, column=2, padx=10, pady=10)

file_list.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
delete_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Run the application
root.mainloop()
