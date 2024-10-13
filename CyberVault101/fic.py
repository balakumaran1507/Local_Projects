import hashlib
import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

# Function to calculate the SHA-256 hash of a file
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
    except FileNotFoundError:
        return None  # Return None if file not found
    return sha256.hexdigest()

# Function to generate hashes for all files in a directory
def generate_hashes(directory, hash_file):
    with open(hash_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_hash(file_path)
                if file_hash:
                    f.write(f"{file_path},{file_hash}\n")
                    log_output(f"Hash generated for {file_path}")

# Function to verify the integrity of files based on saved hashes
def verify_integrity(hash_file):
    try:
        with open(hash_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                file_path, original_hash = line.strip().split(',')
                current_hash = calculate_hash(file_path)

                if current_hash is None:
                    log_output(f"File missing: {file_path}", 'error')
                elif current_hash != original_hash:
                    log_output(f"File tampered: {file_path}", 'error')
                else:
                    log_output(f"File intact: {file_path}", 'success')
    except FileNotFoundError:
        messagebox.showerror("Error", "Hash file not found.")

# Function to log output to the scrolled text box
def log_output(message, tag=None):
    output_box.insert(tk.END, f"{message}\n", tag)
    output_box.see(tk.END)

# Function to select a directory
def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

# Function to select a hash file
def select_hash_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        hash_file_entry.delete(0, tk.END)
        hash_file_entry.insert(0, file_path)

# Function to trigger hash generation
def start_generate_hashes():
    directory = directory_entry.get()
    hash_file = hash_file_entry.get()
    if directory and hash_file:
        generate_hashes(directory, hash_file)
        messagebox.showinfo("Success", "Hashes generated successfully!")
    else:
        messagebox.showerror("Error", "Please select a directory and hash file.")

# Function to trigger integrity check
def start_verify_integrity():
    hash_file = hash_file_entry.get()
    if hash_file:
        verify_integrity(hash_file)
    else:
        messagebox.showerror("Error", "Please select a hash file.")

# Create the main window
root = tk.Tk()
root.title("File Integrity Checker")
root.geometry("500x400")
root.configure(bg='#003300')  # Dark green background

# Create labels and input fields
directory_label = tk.Label(root, text="Select Directory:", bg='#003300', fg='white', font=("Arial", 12))
directory_label.grid(row=0, column=0, padx=10, pady=10)

directory_entry = tk.Entry(root, font=("Arial", 12), width=30)
directory_entry.grid(row=0, column=1, padx=10, pady=10)

directory_button = tk.Button(root, text="Browse", command=select_directory, bg='#006600', fg='white', font=("Arial", 12))
directory_button.grid(row=0, column=2, padx=10, pady=10)

hash_file_label = tk.Label(root, text="Select Hash File:", bg='#003300', fg='white', font=("Arial", 12))
hash_file_label.grid(row=1, column=0, padx=10, pady=10)

hash_file_entry = tk.Entry(root, font=("Arial", 12), width=30)
hash_file_entry.grid(row=1, column=1, padx=10, pady=10)

hash_file_button = tk.Button(root, text="Browse", command=select_hash_file, bg='#006600', fg='white', font=("Arial", 12))
hash_file_button.grid(row=1, column=2, padx=10, pady=10)

# Create buttons for generating and verifying hashes
generate_button = tk.Button(root, text="Generate Hashes", command=start_generate_hashes, bg='#006600', fg='white', font=("Arial", 12))
generate_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

verify_button = tk.Button(root, text="Verify Integrity", command=start_verify_integrity, bg='#006600', fg='white', font=("Arial", 12))
verify_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Create a scrolled text box to show the log output
output_box = scrolledtext.ScrolledText(root, height=10, width=55, font=("Arial", 10), bg='#004400', fg='white')
output_box.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Style tags for log messages
output_box.tag_config('success', foreground='lime')
output_box.tag_config('error', foreground='red')

# Run the application
root.mainloop()
