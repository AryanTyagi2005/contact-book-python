import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import mysql.connector

class ContactBook:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        # Connect to the MySQL database
        self.db = mysql.connector.connect(host="localhost", user="root", password="1234", database="varshithdb")
        self.cursor = self.db.cursor()

        self.create_contact_book_tab()
        
    def create_contact_book_tab(self):
        # Create the frame for the contact book
        self.contact_book_frame = ttk.Frame(self.root)
        self.contact_book_frame.pack()

         # Add a title label
        label_title = tk.Label(self.contact_book_frame)
        label_title.pack(pady=10)

        # Create a listbox to display contacts
        self.contact_list = tk.Listbox(self.contact_book_frame)
        self.contact_list.pack(fill="both", expand=True)

        # Load contacts for the user
        self.update_contact_list()

        # Buttons for managing contacts
        btn_add_contact = tk.Button(self.contact_book_frame, text="Add Contact", command=self.add_contact)
        btn_add_contact.pack()

        btn_edit_contact = tk.Button(self.contact_book_frame, text="Edit Contact", command=self.edit_contact)
        btn_edit_contact.pack()

        btn_delete_contact = tk.Button(self.contact_book_frame, text="Delete Contact", command=self.delete_contact)
        btn_delete_contact.pack()

        # Logout button
        btn_logout = tk.Button(self.contact_book_frame, text="Logout", command=self.logout)
        btn_logout.pack()

    def update_contact_list(self):
         # Clear existing contacts in the listbox and fetch new contacts for the user from the database
        self.contact_list.delete(0, "end")
        self.cursor.execute("SELECT * FROM contacts WHERE username = %s", (self.username,))
        contacts = self.cursor.fetchall()
        for contact in contacts:
            self.contact_list.insert("end", contact[2]) # Display contact name

        # Methods for adding, editing, and deleting contacts...
    def add_contact(self):
        contact_name = simpledialog.askstring("Add Contact", "Enter the contact name:")
        contact_email = simpledialog.askstring("Add Contact", "Enter the contact email:")
        contact_phone_number = simpledialog.askstring("Add Contact", "Enter the contact phone number:")
        contact_phone_number = str(contact_phone_number)[:10]

        self.cursor.execute("INSERT INTO contacts (username, name, email, phone_number) VALUES (%s, %s, %s, %s)",
                            (self.username, contact_name, contact_email, contact_phone_number))
        self.db.commit()
        self.contact_list.insert("end", contact_name)

    def edit_contact(self):
        selected_indices = self.contact_list.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        selected_contact = self.contact_list.get(selected_index)

        self.cursor.execute("SELECT email, phone_number FROM contacts WHERE username = %s AND name = %s",
                            (self.username, selected_contact))
        existing_details = self.cursor.fetchone()
        if not existing_details:
            return

        contact_name = simpledialog.askstring("Edit Contact", "Enter the contact name:", initialvalue=selected_contact)
        if contact_name is None:
            return

        contact_email = simpledialog.askstring("Edit Contact", "Enter the contact email:", initialvalue=existing_details[0])
        if contact_email is None:
            return

        contact_phone_number = simpledialog.askstring("Edit Contact", "Enter the contact phone number:",
                                                      initialvalue=existing_details[1])
        contact_phone_number = str(contact_phone_number)[:14]

        self.cursor.execute("UPDATE contacts SET name = %s, email = %s, phone_number = %s WHERE username = %s AND name = %s",
                            (contact_name, contact_email, contact_phone_number, self.username, selected_contact))
        self.db.commit()
        self.contact_list.delete(selected_index)
        self.contact_list.insert(selected_index, contact_name)

    def delete_contact(self):
        selected_indices = self.contact_list.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        selected_contact = self.contact_list.get(selected_index)

        self.cursor.execute("DELETE FROM contacts WHERE username = %s AND name = %s", (self.username, selected_contact))
        self.db.commit()
        self.contact_list.delete(selected_index)

    def logout(self):
        # Close the ContactBook window and go back to the main application window
        self.root.destroy()  # Close the ContactBook window
        root.deiconify()  # Restore the main application window
          # Open the login tab

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Spectrum")
        self.root.geometry("600x400")  # Set the width and height according to your preference
        
        self.create_tabs() # Initialize the application

    def create_tabs(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Frames for registration and login
        self.register_frame = ttk.Frame(self.notebook)
        self.login_frame = ttk.Frame(self.notebook)

        # Add registration and login frames to the notebook
        self.notebook.add(self.register_frame, text='Register User')
        self.notebook.add(self.login_frame, text='Log In')

        # Create the registration and login tabs
        self.create_register_tab()
        self.create_login_tab()

    def create_register_tab(self):
        label_register = tk.Label(self.register_frame, text="Register User", font=("Arial", 16))
        label_register.pack(pady=10)

        label_username = tk.Label(self.register_frame, text="Username:")
        label_username.pack()
        self.entry_username = tk.Entry(self.register_frame)
        self.entry_username.pack()

        label_password = tk.Label(self.register_frame, text="Password:")
        label_password.pack()
        self.entry_password = tk.Entry(self.register_frame, show="*")
        self.entry_password.pack()

        btn_signup = tk.Button(self.register_frame, text="Sign Up", command=self.signup)
        btn_signup.pack()

        label_have_account = tk.Label(self.register_frame, text="Already have an account?")
        label_have_account.pack()
        btn_login = tk.Button(self.register_frame, text="Log In", command=self.show_login_tab)
        btn_login.pack()

    def create_login_tab(self):
        label_login = tk.Label(self.login_frame, text="Log In", font=("Arial", 16))
        label_login.pack(pady=10)

        label_username_login = tk.Label(self.login_frame, text="Username:")
        label_username_login.pack()
        self.entry_username_login = tk.Entry(self.login_frame)
        self.entry_username_login.pack()

        label_password_login = tk.Label(self.login_frame, text="Password:")
        label_password_login.pack()
        self.entry_password_login = tk.Entry(self.login_frame, show="*")
        self.entry_password_login.pack()

        btn_login = tk.Button(self.login_frame, text="Log In", command=self.login)
        btn_login.pack()

        label_no_account = tk.Label(self.login_frame, text="Don't have an account?")
        label_no_account.pack()
        btn_signup = tk.Button(self.login_frame, text="Sign Up", command=self.show_register_tab)
        btn_signup.pack()

    # Methods to create registration and login tabs...
    def show_register_tab(self):
        # Show the registration tab
        self.notebook.select(self.register_frame)

    def show_login_tab(self):
        # Show the login tab
        self.notebook.select(self.login_frame)

    def signup(self):
        # Sign up a new user and display a success message or error
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username and password:
            db = mysql.connector.connect(host="localhost", user="root", password="1234", database="varshithdb")
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            db.close()
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Please enter both username and password")

    def login(self):
        # Login a user and display the contact book or error
        username = self.entry_username_login.get()
        password = self.entry_password_login.get()

        if username and password:
            db = mysql.connector.connect(host="localhost", user="root", password="1234", database="varshithdb")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            db.close()

            if user:
                self.notebook.forget(self.login_frame)
                contact_book = ContactBook(self.notebook, username)
                self.notebook.add(contact_book.contact_book_frame, text='Contact Book')
                self.notebook.select(contact_book.contact_book_frame)
            else:
                messagebox.showerror("Error", "Invalid credentials")
        else:
            messagebox.showerror("Error", "Please enter both username and password")

# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()