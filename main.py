import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import os
# -------------------- Database Setup Functions -------------------- #
def setup_database():
    """
    Sets up the library_management database and its tables.
    """
    try:
        # Connect to MySQL server without specifying a database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Jeshu2003'  # Update with your MySQL password
        )
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_management")
        print("Database 'library_management' ensured.")

        # Use the created database
        cursor.execute("USE library_management")

        # Create 'library_items' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS library_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                category ENUM('Book', 'Magazine', 'DVD') NOT NULL,
                available_copies INT NOT NULL DEFAULT 0,
                total_copies INT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("Table 'library_items' ensured.")

        # Create 'users' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        print("Table 'users' ensured.")

        # Create 'transactions' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_id INT NOT NULL,
                user_id INT NOT NULL,
                transaction_type ENUM('checkout', 'return') NOT NULL,
                transaction_date DATETIME NOT NULL,
                FOREIGN KEY (item_id) REFERENCES library_items(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        print("Table 'transactions' ensured.")

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error setting up database: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
# -------------------- Library Management System Class -------------------- #
class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1920x1080")  # Increased size for better layout
        self.root.resizable(True,True)  # Prevent window resizing

        # Load Background Image
        self.bg_image = self.load_background("assets/backgrounds/background.jpg")

        # Create Canvas
        self.canvas = tk.Canvas(root, width=1000, height=700)
        self.canvas.pack(fill="both", expand=True)

        # Add Background Image to Canvas
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Create a Frame to hold other widgets
        self.frame = tk.Frame(self.canvas, bg='white', padx=20, pady=20)
        self.canvas.create_window(500, 350, window=self.frame)  # Center the frame in the canvas

        # Load Icons
        self.add_icon = self.load_icon("assets/icons/add_icon.png")
        self.checkout_icon = self.load_icon("assets/icons/checkout_icon.png")
        self.return_icon = self.load_icon("assets/icons/return_icon.png")
        self.search_icon = self.load_icon("assets/icons/search_icon.png")
        self.delete_icon = self.load_icon("assets/icons/delete_icon.png")
        self.manage_users_icon = self.load_icon("assets/icons/manage_users_icon.png")

        # Create Notebook and Tabs
        self.create_widgets()

    def load_background(self, path):
        """
        Loads and resizes the background image.
        """
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Background image not found at {path}")
            self.root.destroy()
        try:
            image = Image.open(path)
            image = image.resize((1920,1080), Image.LANCZOS)  # Resize to fit the window
            return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")
            self.root.destroy()

    def load_icon(self, path):
        """
        Loads and resizes the icon image.
        """
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Icon image not found at {path}")
            self.root.destroy()
        try:
            image = Image.open(path)
            image = image.resize((20, 20), Image.LANCZOS)  # Resize the icon
            return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load icon '{path}': {e}")
            self.root.destroy()

    def create_widgets(self):
        """
        Creates the notebook and adds all tabs.
        """
        self.tab_control = ttk.Notebook(self.frame)

        # Define tabs
        self.add_item_tab = ttk.Frame(self.tab_control)
        self.check_out_tab = ttk.Frame(self.tab_control)
        self.return_item_tab = ttk.Frame(self.tab_control)
        self.search_tab = ttk.Frame(self.tab_control)
        self.delete_tab = ttk.Frame(self.tab_control)
        self.manage_users_tab = ttk.Frame(self.tab_control)  # New tab for managing users

        # Add tabs with icons
        self.tab_control.add(self.add_item_tab, text='Add Item', image=self.add_icon, compound='left')
        self.tab_control.add(self.check_out_tab, text='Check Out', image=self.checkout_icon, compound='left')
        self.tab_control.add(self.return_item_tab, text='Return Item', image=self.return_icon, compound='left')
        self.tab_control.add(self.search_tab, text='Search Item', image=self.search_icon, compound='left')
        self.tab_control.add(self.delete_tab, text='Delete Item/User', image=self.delete_icon, compound='left')
        self.tab_control.add(self.manage_users_tab, text='Manage Users', image=self.manage_users_icon, compound='left')  # Adding the new tab

        self.tab_control.pack(expand=1, fill='both')

        # Setup each tab
        self.setup_add_item_tab()
        self.setup_check_out_tab()
        self.setup_return_item_tab()
        self.setup_search_tab()
        self.setup_delete_tab()
        self.setup_manage_users_tab()  # Setup the new tab

    def setup_add_item_tab(self):
        """
        Sets up the Add Item tab.
        """
        padding_options = {'padx': 5, 'pady': 5}

        # Labels and entries
        self.create_label_entry(self.add_item_tab, "Title", 0, **padding_options)
        self.title_entry = ttk.Entry(self.add_item_tab)
        self.title_entry.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        self.create_label_entry(self.add_item_tab, "Author", 1, **padding_options)
        self.author_entry = ttk.Entry(self.add_item_tab)
        self.author_entry.grid(column=1, row=1, padx=5, pady=5, sticky='ew')

        self.create_label_entry(self.add_item_tab, "Category", 2, **padding_options)
        self.category_entry = ttk.Combobox(self.add_item_tab, values=['Book', 'Magazine', 'DVD'], state='readonly')
        self.category_entry.grid(column=1, row=2, padx=5, pady=5, sticky='ew')

        self.create_label_entry(self.add_item_tab, "Available Copies", 3, **padding_options)
        self.available_copies_entry = ttk.Entry(self.add_item_tab)
        self.available_copies_entry.grid(column=1, row=3, padx=5, pady=5, sticky='ew')

        self.create_label_entry(self.add_item_tab, "Total Copies", 4, **padding_options)
        self.total_copies_entry = ttk.Entry(self.add_item_tab)
        self.total_copies_entry.grid(column=1, row=4, padx=5, pady=5, sticky='ew')

        # Configure grid columns
        self.add_item_tab.columnconfigure(1, weight=1)

        # Add Button
        add_button = ttk.Button(self.add_item_tab, text="Add Item", command=self.add_item)
        add_button.grid(column=0, row=5, columnspan=2, pady=10)

    def setup_check_out_tab(self):
        """
        Sets up the Check Out tab.
        """
        padding_options = {'padx': 5, 'pady': 5}

        # Labels and entries
        self.create_label_entry(self.check_out_tab, "Item ID", 0, **padding_options)
        self.item_id_entry_checkout = ttk.Entry(self.check_out_tab)
        self.item_id_entry_checkout.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        self.create_label_entry(self.check_out_tab, "User ID", 1, **padding_options)
        self.user_id_entry_checkout = ttk.Entry(self.check_out_tab)
        self.user_id_entry_checkout.grid(column=1, row=1, padx=5, pady=5, sticky='ew')

        # Checkout Button
        checkout_button = ttk.Button(self.check_out_tab, text="Check Out", command=self.check_out_item)
        checkout_button.grid(column=0, row=2, columnspan=2, pady=10)

    def setup_return_item_tab(self):
        """
        Sets up the Return Item tab.
        """
        padding_options = {'padx': 5, 'pady': 5}

        # Labels and entries
        self.create_label_entry(self.return_item_tab, "Item ID", 0, **padding_options)
        self.item_id_entry_return = ttk.Entry(self.return_item_tab)
        self.item_id_entry_return.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        self.create_label_entry(self.return_item_tab, "User ID", 1, **padding_options)
        self.user_id_entry_return = ttk.Entry(self.return_item_tab)
        self.user_id_entry_return.grid(column=1, row=1, padx=5, pady=5, sticky='ew')

        # Return Button
        return_button = ttk.Button(self.return_item_tab, text="Return Item", command=self.return_item)
        return_button.grid(column=0, row=2, columnspan=2, pady=10)

    def setup_search_tab(self):
        """
        Sets up the Search Item tab.
        """
        padding_options = {'padx': 5, 'pady': 5}

        # Labels and entries
        self.create_label_entry(self.search_tab, "Search by Title/Author", 0, **padding_options)
        self.search_entry = ttk.Entry(self.search_tab)
        self.search_entry.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        # Search Button
        search_button = ttk.Button(self.search_tab, text="Search", command=self.search_item)
        search_button.grid(column=0, row=1, columnspan=2, pady=10)

    def setup_delete_tab(self):
        """
        Sets up the Delete Item/User tab.
        """
        padding_options = {'padx': 5, 'pady': 5}

        # Labels and entries
        self.create_label_entry(self.delete_tab, "Item/User ID", 0, **padding_options)
        self.delete_id_entry = ttk.Entry(self.delete_tab)
        self.delete_id_entry.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        # Delete Button
        delete_button = ttk.Button(self.delete_tab, text="Delete", command=self.delete_item_user)
        delete_button.grid(column=0, row=1, columnspan=2, pady=10)

    def setup_manage_users_tab(self):
        """
        Sets up the Manage Users tab.
        """
        padding_options = {'padx': 5, 'pady': 5}

        # Labels and entries
        self.create_label_entry(self.manage_users_tab, "User Name", 0, **padding_options)
        self.user_name_entry = ttk.Entry(self.manage_users_tab)
        self.user_name_entry.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        self.create_label_entry(self.manage_users_tab, "Email", 1, **padding_options)
        self.user_email_entry = ttk.Entry(self.manage_users_tab)
        self.user_email_entry.grid(column=1, row=1, padx=5, pady=5, sticky='ew')

        # Add User Button
        add_user_button = ttk.Button(self.manage_users_tab, text="Add User", command=self.add_user)
        add_user_button.grid(column=0, row=2, columnspan=2, pady=10)

        # Load Users Button
        load_users_button = ttk.Button(self.manage_users_tab, text="Load Users", command=self.load_users)
        load_users_button.grid(column=0, row=3, columnspan=2, pady=10)

        # Users Listbox
        self.users_listbox = tk.Listbox(self.manage_users_tab)
        self.users_listbox.grid(column=0, row=4, columnspan=2, padx=5, pady=5, sticky='ew')

    def create_label_entry(self, parent, text, row, **options):
        """
        Creates a label and entry widget.
        """
        label = ttk.Label(parent, text=text)
        label.grid(column=0, row=row, **options)

    def add_item(self):
        """
        Adds an item to the database.
        """
        title = self.title_entry.get()
        author = self.author_entry.get()
        category = self.category_entry.get()
        available_copies = self.available_copies_entry.get()
        total_copies = self.total_copies_entry.get()

        if not all([title, author, category, available_copies, total_copies]):
            messagebox.showwarning("Input Error", "All fields must be filled out.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jeshu2003',  # Update with your MySQL password
                database='library_management'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO library_items (title, author, category, available_copies, total_copies) VALUES (%s, %s, %s, %s, %s)", 
                           (title, author, category, available_copies, total_copies))
            conn.commit()
            messagebox.showinfo("Success", "Item added successfully!")
            self.clear_add_item_fields()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add item: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def clear_add_item_fields(self):
        """
        Clears the fields in the Add Item tab.
        """
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.set('')
        self.available_copies_entry.delete(0, tk.END)
        self.total_copies_entry.delete(0, tk.END)

    def check_out_item(self):
        """
        Checks out an item from the library.
        """
        item_id = self.item_id_entry_checkout.get()
        user_id = self.user_id_entry_checkout.get()

        if not all([item_id, user_id]):
            messagebox.showwarning("Input Error", "Both Item ID and User ID must be filled out.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jeshu2003',
                database='library_management'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transactions (item_id, user_id, transaction_type, transaction_date) VALUES (%s, %s, %s, NOW())", 
                           (item_id, user_id, 'checkout'))
            conn.commit()
            messagebox.showinfo("Success", "Item checked out successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to check out item: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def return_item(self):
        """
        Returns an item to the library.
        """
        item_id = self.item_id_entry_return.get()
        user_id = self.user_id_entry_return.get()

        if not all([item_id, user_id]):
            messagebox.showwarning("Input Error", "Both Item ID and User ID must be filled out.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jeshu2003',
                database='library_management'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transactions (item_id, user_id, transaction_type, transaction_date) VALUES (%s, %s, %s, NOW())", 
                           (item_id, user_id, 'return'))
            conn.commit()
            messagebox.showinfo("Success", "Item returned successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to return item: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def search_item(self):
        """
        Searches for an item in the library.
        """
        search_term = self.search_entry.get()

        if not search_term:
            messagebox.showwarning("Input Error", "Search term must be filled out.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jeshu2003',
                database='library_management'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM library_items WHERE title LIKE %s OR author LIKE %s", 
                           (f'%{search_term}%', f'%{search_term}%'))
            results = cursor.fetchall()

            if results:
                result_string = "\n".join([f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}" for row in results])
                messagebox.showinfo("Search Results", result_string)
            else:
                messagebox.showinfo("Search Results", "No items found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to search items: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_item_user(self):
        """
        Deletes an item or user from the database.
        """
        delete_id = self.delete_id_entry.get()

        if not delete_id:
            messagebox.showwarning("Input Error", "ID must be filled out.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jeshu2003',
                database='library_management'
            )
            cursor = conn.cursor()

            # Check if it's an item or user based on the existence in respective tables
            cursor.execute("SELECT id FROM library_items WHERE id = %s", (delete_id,))
            if cursor.fetchone():
                cursor.execute("DELETE FROM library_items WHERE id = %s", (delete_id,))
                conn.commit()
                messagebox.showinfo("Success", "Item deleted successfully!")
            else:
                cursor.execute("SELECT id FROM users WHERE id = %s", (delete_id,))
                if cursor.fetchone():
                    cursor.execute("DELETE FROM users WHERE id = %s", (delete_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "User deleted successfully!")
                else:
                    messagebox.showwarning("Error", "Item/User ID not found.")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to delete: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def add_user(self):
        """
        Adds a user to the database.
        """
        name = self.user_name_entry.get()
        email = self.user_email_entry.get()

        if not all([name, email]):
            messagebox.showwarning("Input Error", "Both Name and Email must be filled out.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jeshu2003',
                database='library_management'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "User added successfully!")
            self.clear_user_fields()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add user: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def clear_user_fields(self):
        """
        Clears the fields in the Manage Users tab.
        """
        self.user_name_entry.delete(0, tk.END)
        self.user_email_entry.delete(0, tk.END)

    def load_users(self):
        """
        Loads users from the database and displays them in the listbox.
        """
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Jeshu2003',
                database='library_management'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            results = cursor.fetchall()

            self.users_listbox.delete(0, tk.END)  # Clear previous entries
            for row in results:
                self.users_listbox.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load users: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    
# -------------------- Main Program Execution -------------------- #
if __name__ == "__main__":
    setup_database()  # Ensure the database and tables are set up
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()