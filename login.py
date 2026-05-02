import mysql.connector as psq
import tkinter 
from tkinter import messagebox

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'charan',
    'database': 'sandhya'
}

def init_db():
    """Creates the table if it doesn't exist."""
    con = psq.connect(**db_config)
    cur = con.cursor()
    # Fixed syntax: added 'S' to EXISTS and closed the parenthesis
    cur.execute("""
        CREATE TABLE IF NOT EXISTS login (
            username VARCHAR(30) PRIMARY KEY,
            password VARCHAR(20) NOT NULL
        )
    """)
    con.commit()
    con.close()

def signup():
    username = enteruser.get()
    password = enterpass.get()
    
    if not username or not password:
        messagebox.showwarning("Error", "Fields cannot be empty")
        return

    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        # Use parameterized queries (%s) to prevent SQL Injection
        query = "INSERT INTO login VALUES(username, password) "
        cur.execute(query, (username, password))
        con.commit()
        con.close()
        messagebox.showinfo("Success", f"Account created for {username}")
    except psq.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

def checklogin(username, password):
    con = psq.connect(**db_config)
    cur = con.cursor()
    # Parameterized query for security
    query = "SELECT * FROM login WHERE username = %s AND password = %s"
    cur.execute(query, (username, password))
    s = cur.fetchone()
    con.close()
    return s

def login_action():
    user = enteruser.get()
    pw = enterpass.get()
    
    if checklogin(user, pw):
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Failed", "Invalid Username or Password")

# Initialize DB on startup
init_db()

# UI Setup
base = tkinter.Tk()
base.title("Secure Login")
base.geometry("300x300")

tkinter.Label(base, text="Username").pack(pady=(20, 0))
enteruser = tkinter.Entry(base)
enteruser.pack()

tkinter.Label(base, text="Password").pack(pady=(10, 0))
enterpass = tkinter.Entry(base, show="*") # Hides password characters
enterpass.pack()

tkinter.Button(base, text="Login", command=login_action, width=15).pack(pady=20)
tkinter.Button(base, text="Signup", command=signup, width=15).pack(pady=5)

base.mainloop()