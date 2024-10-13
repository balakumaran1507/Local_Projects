import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File/Folder Encryption App")
        self.root.geometry("400x400")  # Fixed window size
        self.root.config(bg="#1a1a1a")  # Cyber theme background color
        
        # Key generation
        self.key = None
        self.key_file = 'secret.key'
        
        # Style the buttons to match the cyber theme
        button_style = {"font": ("Helvetica", 14), "fg": "#00ff00", "bg": "#333333", "activebackground": "#4d4d4d", "relief": "flat", "width": 25}

        # Generate and save key button
        self.generate_key_button = tk.Button(root, text="Generate Key", command=self.generate_key, **button_style)
        self.generate_key_button.pack(pady=10)
        
        # Encrypt File button
        self.encrypt_file_button = tk.Button(root, text="Encrypt File", command=self.encrypt_file, **button_style)
        self.encrypt_file_button.pack(pady=10)
        
        # Decrypt File button
        self.decrypt_file_button = tk.Button(root, text="Decrypt File", command=self.decrypt_file, **button_style)
        self.decrypt_file_button.pack(pady=10)
        
        # Encrypt Folder button
        self.encrypt_folder_button = tk.Button(root, text="Encrypt Folder", command=self.encrypt_folder, **button_style)
        self.encrypt_folder_button.pack(pady=10)
        
        # Decrypt Folder button
        self.decrypt_folder_button = tk.Button(root, text="Decrypt Folder", command=self.decrypt_folder, **button_style)
        self.decrypt_folder_button.pack(pady=10)
        
        # Add a footer label with a cyber theme
        footer_label = tk.Label(root, text="© 2024 Cyber Vault", font=("Helvetica", 10), fg="#00ff00", bg="#1a1a1a")
        footer_label.pack(side="bottom", pady=10)

    def generate_key(self):
        """Generate a key and save it."""
        self.key = Fernet.generate_key()
        with open(self.key_file, 'wb') as file:
            file.write(self.key)
        messagebox.showinfo("Success", "Key generated and saved to 'secret.key'")

    def load_key(self):
        """Load the encryption key."""
        if not os.path.exists(self.key_file):
            messagebox.showerror("Error", "Key file does not exist.")
            return None
        with open(self.key_file, 'rb') as file:
            return file.read()
    
    def encrypt_file(self):
        """Encrypt a file."""
        key = self.load_key()
        if not key:
            return
        file_path = filedialog.askopenfilename(title="Select file to encrypt")
        if not file_path:
            return
        
        fernet = Fernet(key)
        with open(file_path, 'rb') as file:
            data = file.read()
        
        encrypted_data = fernet.encrypt(data)
        
        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)
        
        os.remove(file_path)
        messagebox.showinfo("Success", f"File encrypted as '{encrypted_file_path}'")

    def decrypt_file(self):
        """Decrypt a file."""
        key = self.load_key()
        if not key:
            return
        file_path = filedialog.askopenfilename(title="Select file to decrypt", filetypes=[("Encrypted Files", "*.enc")])
        if not file_path:
            return
        
        fernet = Fernet(key)
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = fernet.decrypt(encrypted_data)
        
        original_file_path = file_path.rsplit('.', 1)[0]
        with open(original_file_path, 'wb') as file:
            file.write(decrypted_data)
        
        os.remove(file_path)
        messagebox.showinfo("Success", f"File decrypted as '{original_file_path}'")

    def encrypt_folder(self):
        """Encrypt all files in a folder."""
        key = self.load_key()
        if not key:
            return
        folder_path = filedialog.askdirectory(title="Select folder to encrypt")
        if not folder_path:
            return
        
        fernet = Fernet(key)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                encrypted_data = fernet.encrypt(data)
                
                encrypted_file_path = file_path + '.enc'
                with open(encrypted_file_path, 'wb') as f:
                    f.write(encrypted_data)
                
                os.remove(file_path)
                
        messagebox.showinfo("Success", "All files in the folder have been encrypted")

    def decrypt_folder(self):
        """Decrypt all files in a folder."""
        key = self.load_key()
        if not key:
            return
        folder_path = filedialog.askdirectory(title="Select folder to decrypt")
        if not folder_path:
            return
        
        fernet = Fernet(key)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.enc'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        encrypted_data = f.read()
                    
                    decrypted_data = fernet.decrypt(encrypted_data)
                    
                    original_file_path = file_path.rsplit('.', 1)[0]
                    with open(original_file_path, 'wb') as f:
                        f.write(decrypted_data)
                    
                    os.remove(file_path)
                    
        messagebox.showinfo("Success", "All files in the folder have been decrypted")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
