import tkinter as tk
from tkinter import messagebox
import socket
import threading

class ServerApp:
    def __init__(self, root):
        self.root = root
        self.server_socket = None
        self.is_running = False
        self.connection_thread = None
        
        self.root.title("Simple TCP Server")
        self.root.geometry("400x300")
        self.root.configure(bg="#333")

        # UI Components
        title_font = ("Arial", 16, "bold")
        label_font = ("Arial", 12)
        button_font = ("Arial", 12, "bold")

        # Title
        tk.Label(root, text="TCP Server", font=title_font, bg="#333", fg="#fff").pack(pady=10)

        # Port Entry
        tk.Label(root, text="Port Number:", font=label_font, bg="#333", fg="#fff").pack(pady=5)
        self.port_entry = tk.Entry(root, font=label_font)
        self.port_entry.pack(pady=5)

        # Start/Stop Button
        self.start_button = tk.Button(root, text="Start Server", font=button_font, bg="#00bfff", fg="#fff", command=self.toggle_server)
        self.start_button.pack(pady=20)

        # Server Log
        self.log_area = tk.Text(root, height=8, width=40, state='disabled')
        self.log_area.pack(pady=10)

    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.config(state='disabled')

    def toggle_server(self):
        if not self.is_running:
            try:
                port = int(self.port_entry.get())
                self.start_server(port)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid port number.")
        else:
            self.stop_server()

    def start_server(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind(('0.0.0.0', port))
            self.server_socket.listen(5)
            self.is_running = True
            self.start_button.config(text="Stop Server", bg="#ff6347")
            self.log_message(f"Server started on port {port}. Listening for connections...")

            # Start a new thread for accepting connections
            self.connection_thread = threading.Thread(target=self.accept_connections, daemon=True)
            self.connection_thread.start()
        except socket.error as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")

    def accept_connections(self):
        while self.is_running:
            try:
                client_socket, addr = self.server_socket.accept()
                self.log_message(f"Connection from {addr} established.")
                client_socket.send(b"Hello, World!")
                client_socket.close()
                self.log_message(f"Connection from {addr} closed.")
            except Exception as e:
                self.log_message(f"Error: {e}")
                break

    def stop_server(self):
        self.is_running = False
        if self.server_socket:
            self.server_socket.close()
        self.start_button.config(text="Start Server", bg="#00bfff")
        self.log_message("Server stopped.")

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()
