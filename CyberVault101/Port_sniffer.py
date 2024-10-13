import socket
import tkinter as tk
from tkinter import scrolledtext

# Function to get the current network IP address
def get_current_ip():
    try:
        # Create a socket and connect to a public address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        current_ip = s.getsockname()[0]
        s.close()
        return current_ip
    except Exception as e:
        return "Unable to get IP"

# Function to scan ports
def port_scanner(ip, ports):
    output_box.delete(1.0, tk.END)  # Clear the output box
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            output_box.insert(tk.END, f"Port {port}: OPEN\n", 'open')
        else:
            output_box.insert(tk.END, f"Port {port}: CLOSED\n", 'closed')
        sock.close()

# Function to trigger port scan
def start_scan():
    ip = ip_entry.get()
    ports = port_entry.get().split(',')
    ports = [int(port.strip()) for port in ports]
    port_scanner(ip, ports)

# Create the main window
root = tk.Tk()
root.title("Port Scanner")
root.configure(bg='#003300')  # Dark green background

# Set the default IP address to the current network IP
default_ip = get_current_ip()

# Create a label for the IP Address input
ip_label = tk.Label(root, text="Target IP:", bg='#003300', fg='white', font=("Arial", 12))
ip_label.grid(row=0, column=0, padx=10, pady=10)

# Create an entry box for the IP Address with the default IP
ip_entry = tk.Entry(root, font=("Arial", 12))
ip_entry.grid(row=0, column=1, padx=10, pady=10)
ip_entry.insert(0, default_ip)  # Set default IP

# Create a label for Ports input
port_label = tk.Label(root, text="Ports (comma-separated):", bg='#003300', fg='white', font=("Arial", 12))
port_label.grid(row=1, column=0, padx=10, pady=10)

# Create an entry box for the Ports
port_entry = tk.Entry(root, font=("Arial", 12))
port_entry.grid(row=1, column=1, padx=10, pady=10)

# Create a button to start the scan
scan_button = tk.Button(root, text="Scan", command=start_scan, bg='#006600', fg='white', font=("Arial", 12))
scan_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create a scrolled text box to show the scan results
output_box = scrolledtext.ScrolledText(root, height=10, width=40, font=("Arial", 10), bg='#004400', fg='white')
output_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Style tags for open and closed ports
output_box.tag_config('open', foreground='lime')
output_box.tag_config('closed', foreground='red')

# Run the application
root.mainloop()
