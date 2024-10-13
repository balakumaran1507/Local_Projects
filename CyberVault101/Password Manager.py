import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import string
import pyperclip
import sqlite3

# Create database connection
def create_connection():
    conn = sqlite3.connect('password_manager.db')
    return conn

# Create table if it doesn't exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS passwords (
            website TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add password to the database
def add_password_to_db(website, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO passwords (website, email, password)
        VALUES (?, ?, ?)
    ''', (website, email, password))
    conn.commit()
    conn.close()

# Retrieve passwords from the database
def retrieve_passwords_from_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT website, email, password FROM passwords')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to clear all passwords from the database
def clear_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords')  # Delete all rows
    conn.commit()
    conn.close()
    messagebox.showinfo("Database Cleared", "All passwords have been removed from the database.")

# Setup database and create table
create_table()

window = tk.Tk()
window.title("Password Manager V0.0.1")
window.geometry('440x540')
window.configure(bg='#333333')

# Encrypted login credentials
username = "User123"
password = "password"

def login():
    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        show_password_manager()
    else:
        messagebox.showerror(title="Error", message="Invalid login.")

def show_password_manager():
    frame.pack_forget()
    password_manager_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def add_password():
    website = website_entry.get()
    password = password_new_entry.get()
    email = email_entry.get()
    
    if website and email and password:  # Ensure all fields are filled
        # Add to the database
        add_password_to_db(website, email, password)
        
        messagebox.showinfo("Success", "Password added successfully")
        
        # Clear input fields
        website_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_new_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "All fields must be filled.")

def view_passwords():
    password_window = tk.Toplevel(window)
    password_window.title("Passwords")
    password_window.geometry('600x400')
    password_window.configure(bg='#333333')

    tree = ttk.Treeview(password_window, columns=("Website", "Email", "Password"), show='headings')
    tree.heading("Website", text="Website")
    tree.heading("Email", text="Email")
    tree.heading("Password", text="Password")

    # Pack the treeview widget
    tree.pack(expand=True, fill=tk.BOTH)

    # Retrieve passwords from the database
    rows = retrieve_passwords_from_db()
    if not rows:
        messagebox.showinfo("Info", "No passwords found.")
    
    for website, email, password in rows:
        tree.insert("", "end", values=(website, email, password))

    # Set a scrollbar for the treeview
    scrollbar = ttk.Scrollbar(password_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    pyperclip.copy(password)
    messagebox.showinfo("Generated Password", f"Your generated password is: {password}\n\nThe password has been copied to the clipboard.")

frame = tk.Frame(bg='#333333')

login_label = tk.Label(frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tk.Entry(frame, font=("Arial", 16))
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tk.Button(frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)

login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()

password_manager_frame = tk.Frame(window, bg='#333333')

website_label = tk.Label(password_manager_frame, text="Website", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
website_entry = tk.Entry(password_manager_frame, font=("Arial", 16))
email_label = tk.Label(password_manager_frame, text="Email", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
email_entry = tk.Entry(password_manager_frame, font=("Arial", 16))
password_new_label = tk.Label(password_manager_frame, text="New Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
password_new_entry = tk.Entry(password_manager_frame, show="*", font=("Arial", 16))
add_password_button = tk.Button(password_manager_frame, text="Add Password", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=add_password)
view_passwords_button = tk.Button(password_manager_frame, text="View Passwords", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=view_passwords)
generate_password_button = tk.Button(password_manager_frame, text="Generate Password", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=generate_password)
clear_database_button = tk.Button(password_manager_frame, text="Clear Database", bg="red", fg="#FFFFFF", font=("Arial", 16), command=clear_database)

website_label.grid(row=0, column=0)
website_entry.grid(row=0, column=1, pady=10)
email_label.grid(row=1, column=0)
email_entry.grid(row=1, column=1, pady=10)
password_new_label.grid(row=2, column=0)
password_new_entry.grid(row=2, column=1, pady=10)
add_password_button.grid(row=3, column=0, columnspan=2, pady=10)
view_passwords_button.grid(row=4, column=0, columnspan=2, pady=10)
generate_password_button.grid(row=5, column=0, columnspan=2, pady=10)
clear_database_button.grid(row=6, column=0, columnspan=2, pady=10)  # Added Clear Database button

window.mainloop()
