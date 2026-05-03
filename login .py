import mysql.connector as psq
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------- DATABASE ----------------
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2101',
    'database': 'sandhya'
}

def init_db():
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS userdetails (fullname VARCHAR(30) NOT NULL, age INT, gender VARCHAR(10), email VARCHAR(50), username VARCHAR(50) PRIMARY KEY, password VARCHAR(20), bio VARCHAR(50))")
    con.commit()
    con.close()

# ---------------- SIGNUP ----------------
def user_signup():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    email = email_entry.get()
    bio = bio_entry.get()
    username = user_entry.get()
    password = pass_entry.get()
    confirm = confirm_entry.get()

    if not all([name, age, email, username, password, confirm]):
        messagebox.showerror("Error", "All fields required")
        return

    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number")
        return

    if len(password) <= 4:
        messagebox.showerror("Error", "Password must be > 4 characters")
        return

    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match")
        return

    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO userdetails (fullname, age, gender, email, username, password, bio) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (name, age, gender, email, username, password, bio)
        )
        con.commit()
        con.close()

        messagebox.showinfo("Success", "Account created!")
        show_login_screen()

    except psq.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# ---------------- LOGIN ----------------
def checklogin(username, password):
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("SELECT * FROM userdetails WHERE username=%s AND password=%s", (username, password))
    result = cur.fetchone()
    con.close()
    return result

def login_action():
    user = enteruser.get()
    pw = enterpass.get()

    if checklogin(user, pw):
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Failed", "Invalid Username or Password")

# ---------------- UI ----------------
init_db()

base = tk.Tk()
base.title("Login System")
base.geometry("1200x800")

# Background
try:
    img = Image.open("MOVIE.jpeg")
    bg_photo = ImageTk.PhotoImage(img)

    bg_label = tk.Label(base, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

# ---------------- FRAME SWITCH ----------------
def show_signup_screen():
    login_frame.place_forget()
    signup_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_login_screen():
    signup_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor='center')

# ---------------- LOGIN FRAME ----------------
login_frame = tk.Frame(base, bg='white', bd=2)

tk.Label(login_frame, text="LOGIN", font=('Arial', 30, 'bold')).pack(pady=20)

tk.Label(login_frame, text="Username", font=('Arial', 15)).pack()
enteruser = tk.Entry(login_frame, width=30)
enteruser.pack(pady=10)

tk.Label(login_frame, text="Password", font=('Arial', 15)).pack()
enterpass = tk.Entry(login_frame, width=30, show="*")
enterpass.pack(pady=10)

tk.Button(login_frame, text="Login", command=login_action).pack(pady=20)
tk.Button(login_frame, text="Create Account", command=show_signup_screen).pack()

# ---------------- SIGNUP FRAME ----------------
signup_frame = tk.Frame(base, bg='white', bd=2)

tk.Label(signup_frame, text="SIGN UP", font=('Arial', 30, 'bold')).pack(pady=20)

tk.Label(signup_frame, text="Full Name").pack()
name_entry = tk.Entry(signup_frame, width=30)
name_entry.pack()

tk.Label(signup_frame, text="Age").pack()
age_entry = tk.Entry(signup_frame, width=30)
age_entry.pack()

tk.Label(signup_frame, text="Gender").pack()

gender_var = tk.StringVar(value="Male")
frame = tk.Frame(signup_frame)
frame.pack()

tk.Radiobutton(frame, text="Male", variable=gender_var, value="Male").pack(side="left")
tk.Radiobutton(frame, text="Female", variable=gender_var, value="Female").pack(side="left")
tk.Radiobutton(frame, text="Other", variable=gender_var, value="Other").pack(side="left")

tk.Label(signup_frame, text="Email").pack()
email_entry = tk.Entry(signup_frame, width=30)
email_entry.pack()

tk.Label(signup_frame, text="Bio").pack()
bio_entry = tk.Entry(signup_frame, width=30)
bio_entry.pack()

tk.Label(signup_frame, text="Username").pack()
user_entry = tk.Entry(signup_frame, width=30)
user_entry.pack()

tk.Label(signup_frame, text="Password").pack()
pass_entry = tk.Entry(signup_frame, width=30, show="*")
pass_entry.pack()

tk.Label(signup_frame, text="Confirm Password").pack()
confirm_entry = tk.Entry(signup_frame, width=30, show="*")
confirm_entry.pack()

tk.Button(signup_frame, text="Register", command=user_signup).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=show_login_screen).pack()

# Show login first
show_login_screen()

base.mainloop()