import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

# Define the directory where your scripts are located
SCRIPT_DIR = os.path.abspath('C:\\Users\\balak\\OneDrive\\Desktop\\Projects\\Local_Projects\\CyberVault101')

def run_script(script_name):
    try:
        # Construct the absolute path for the script
        script_path = os.path.join(SCRIPT_DIR, script_name)
        # Run the script using the current Python interpreter
        subprocess.Popen([sys.executable, script_path], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run {script_name}\n{str(e)}")

# Create the main window
root = tk.Tk()
root.title("Cyber Vault Launcher")
root.geometry("400x400")  # Adjusted window size to accommodate the additional button
root.config(bg="#1a1a1a")  # Cyber theme background color

# Create a title label with a cyber theme font and color
title_label = tk.Label(root, text="Cyber Vault Launcher", font=("Helvetica", 18, "bold"), fg="#00ff00", bg="#1a1a1a")
title_label.pack(pady=20)

# Style the buttons to match the cyber theme
button_style = {"font": ("Helvetica", 14), "fg": "#00ff00", "bg": "#333333", "activebackground": "#4d4d4d", "relief": "flat", "width": 20}

# Create and place buttons for each script with cyber theme
button_keylogger = tk.Button(root, text="Run Keylogger", command=lambda: run_script('keylogger_final.py'), **button_style)
button_keylogger.pack(pady=10)

button_encrypt = tk.Button(root, text="Run Encrypt", command=lambda: run_script('Encrpt.py'), **button_style)
button_encrypt.pack(pady=10)

button_password_manager = tk.Button(root, text="Run Password Manager", command=lambda: run_script('Password Manager.py'), **button_style)
button_password_manager.pack(pady=10)

# New button for the Port Sniffer
button_port_sniffer = tk.Button(root, text="Run Port Sniffer", command=lambda: run_script('Port_sniffer.py'), **button_style)
button_port_sniffer.pack(pady=10)

# Add a separator line for aesthetics
separator = tk.Frame(root, height=2, bd=0, bg="#00ff00")
separator.pack(fill="x", pady=10)

# Add a footer label with a cyber theme
footer_label = tk.Label(root, text="© 2024 Cyber Vault", font=("Helvetica", 10), fg="#00ff00", bg="#1a1a1a")
footer_label.pack(side="bottom", pady=10)

# Start the GUI event loop
root.mainloop()
