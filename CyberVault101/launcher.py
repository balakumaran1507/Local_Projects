import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def run_script(script_name):
    try:
        # Construct the absolute path for the script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
        # Run the script using subprocess
        subprocess.Popen(['python', script_path], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {script_name}\n{str(e)}")

# Create the main window
root = tk.Tk()
root.title("Script Launcher")

# Create and place buttons for each script
button_keylogger = tk.Button(root, text="Run Keylogger", command=lambda: run_script('keylogger_final.py'))
button_keylogger.pack(pady=10)

button_encrypt = tk.Button(root, text="Run Encrpt", command=lambda: run_script('Encrpt.py'))
button_encrypt.pack(pady=10)

# Start the GUI event loop
root.mainloop()
