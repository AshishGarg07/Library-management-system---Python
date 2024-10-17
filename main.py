import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector as sql

# MYSQL Connection
def connect_db(password):
    try:
        db = sql.connect(host="localhost", user="root", passwd=password)
        cursor = db.cursor()
        if db.is_connected():
            try:
                cursor.execute("USE pyplm")
                db.commit()
                print("Database connected")
            except:
                cursor.execute("create database pyplm")
                cursor.execute("USE pyplm")
                print("New Database Created")
                db.commit()
                print("Database connected")
            return db, cursor
    except:
        messagebox.showerror("Connection Error", "Could not connect to the database. Check the password or MySQL installation.")
        return None, None

# Initialize the main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("800x600")

# Set a background color
root.configure(bg="#f0e68c")  # Light Khaki background

Admin_Passwd = "admin"

# Main Menu
def start_menu():
    clear_frame()
    label = tk.Label(root, text="WELCOME\n", font=("Arial", 24), bg="#f0e68c", fg="#000000")
    label.place(relx=0.5, rely=0.2, anchor="center")

    admin_btn = tk.Button(root, text="Admin Login", command=admin_login, width=15, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    admin_btn.place(relx=0.5, rely=0.4, anchor="center")

    student_btn = tk.Button(root, text="Student Login", command=student_panel, width=15, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    student_btn.place(relx=0.5, rely=0.5, anchor="center")

    exit_btn = tk.Button(root, text="Exit", command=exit_prog, width=15, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    exit_btn.place(relx=0.5, rely=0.6, anchor="center")

# Clear the current frame
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

# Admin Login
def admin_login():
    password = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')
    if password == Admin_Passwd:
        admin_panel()
    else:
        messagebox.showerror("Error", "Wrong Password!")
        start_menu()

# Admin Panel
def admin_panel():
    clear_frame()
    label = tk.Label(root, text="Admin Portal", font=("Arial", 24), bg="#f0e68c", fg="#000000")
    label.place(relx=0.5, rely=0.2, anchor="center")

    view_btn = tk.Button(root, text="View All Books Issued", command=view_table_data, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    view_btn.place(relx=0.5, rely=0.4, anchor="center")

    edit_btn = tk.Button(root, text="Edit Issued Books Data", command=edit_table_data, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    edit_btn.place(relx=0.5, rely=0.5, anchor="center")

    delete_btn = tk.Button(root, text="Delete Record", command=delete_row, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    delete_btn.place(relx=0.5, rely=0.6, anchor="center")

    back_btn = tk.Button(root, text="Back", command=start_menu, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    back_btn.place(relx=0.5, rely=0.7, anchor="center")

# Student Panel
def student_panel():
    clear_frame()
    label = tk.Label(root, text="Student Portal", font=("Arial", 24), bg="#f0e68c", fg="#000000")
    label.place(relx=0.5, rely=0.2, anchor="center")

    issue_btn = tk.Button(root, text="Issue a New Book", command=issue_book, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    issue_btn.place(relx=0.5, rely=0.4, anchor="center")

    return_btn = tk.Button(root, text="Return a Book", command=return_book, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    return_btn.place(relx=0.5, rely=0.5, anchor="center")

    view_btn = tk.Button(root, text="View all Issued Books", command=view_student_issue_book, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    view_btn.place(relx=0.5, rely=0.6, anchor="center")

    back_btn = tk.Button(root, text="Back", command=start_menu, width=20, height=2, bg="#8b4513", fg="#ffffff", font=("Arial", 12))
    back_btn.place(relx=0.5, rely=0.7, anchor="center")

# Commands (Admin/Student Panel)
def view_table_data():
    query = "SELECT * FROM DATA"
    cursor.execute(query)
    results = cursor.fetchall()
    messagebox.showinfo("Issued Books", "\n".join([f"Student ID: {i[0]}, Book ID: {i[1]}" for i in results]))

def edit_table_data():
    student_id = simpledialog.askinteger("Edit Book", "Enter Student ID:")
    new_book_id = simpledialog.askinteger("Edit Book", "Enter New Book ID:")
    query = f"UPDATE DATA SET Book_ID = {new_book_id} WHERE Student_ID = {student_id}"
    cursor.execute(query)
    db.commit()
    messagebox.showinfo("Success", "Record updated successfully")

def delete_row():
    student_id = simpledialog.askinteger("Delete Record", "Enter Student ID:")
    query = f"DELETE FROM DATA WHERE Student_ID = {student_id}"
    cursor.execute(query)
    db.commit()
    messagebox.showinfo("Success", "Record deleted successfully")

def issue_book():
    student_id = simpledialog.askinteger("Issue Book", "Enter Student ID:")
    book_id = simpledialog.askinteger("Issue Book", "Enter Book UPC Code:")
    query = f"INSERT INTO DATA (Student_ID, Book_ID) VALUES ({student_id}, {book_id})"
    cursor.execute(query)
    db.commit()
    messagebox.showinfo("Success", f"Book {book_id} issued to student {student_id}")

def return_book():
    student_id = simpledialog.askinteger("Return Book", "Enter Student ID:")
    book_id = simpledialog.askinteger("Return Book", "Enter Book ID:")
    query = f"DELETE FROM DATA WHERE Student_ID = {student_id} AND Book_ID = {book_id}"
    cursor.execute(query)
    db.commit()
    messagebox.showinfo("Success", "Book returned successfully")

def view_student_issue_book():
    student_id = simpledialog.askinteger("View Issued Books", "Enter Student ID:")
    query = f"SELECT * FROM DATA WHERE Student_ID = {student_id}"
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        messagebox.showinfo("Issued Books", "\n".join([f"Book ID: {i[1]}" for i in results]))
    else:
        messagebox.showinfo("No Books", "No books issued to this student.")

# Exit Program
def exit_prog():
    cursor.close()
    db.close()
    sys.exit()

# Establish DB Connection
password = simpledialog.askstring("DB Password", "Enter MySQL Password:", show='*')
db, cursor = connect_db(password)

# Start the GUI
start_menu()
root.mainloop()
