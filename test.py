import mysql.connector as psq
import tkinter 
from tkinter import messagebox
from PIL import Image, ImageTk
import os

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
    cur.execute("CREATE TABLE IF NOT EXISTS login (username VARCHAR(30) PRIMARY KEY, password VARCHAR(30))")
    con.commit()
    con.close()



# SIGNING UP BOX
def signup():
    username = signup_user.get()
    password = signup_pass.get()
    if not username or not password:
        messagebox.showwarning("Error", "Fields cannot be empty")
        return
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("INSERT INTO login (username, password) VALUES (%s, %s)",(username,password))
        con.commit()
        con.close()
        messagebox.showinfo("Success", f"Account created for {username}")
        show_login_screen() 
    except psq.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# CHECKS IF SIGNUP U,P IS EQUAL TO LOGIN U,P
def checklogin(username, password):
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
    s = cur.fetchone()
    con.close()
    return s

# LOGIN BOX
def login_action():
    user = enteruser.get()
    pw = enterpass.get()
    if checklogin(user, pw):
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Failed", "Invalid Username or Password")

# Initialize DB
init_db()

# UI Setup
base = tkinter.Tk()
base.title("Secure Login System")
base.geometry("1200x800") 

def show_signup_screen():
    login_frame.place_forget()
    signup_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_login_screen():
    signup_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor='center')


try:
    
    img = Image.open("MOVIE.jpeg")
   
    bg_photo = ImageTk.PhotoImage(img)
    
    bg_label = tkinter.Label(base, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    
except:
    pass

#LOGIN SCREEN FRAME 

login_frame = tkinter.Frame(base, bg='white', bd=2)

tkinter.Label(login_frame, text="LOGIN", font=('Arial', 35, 'bold')).pack(pady=20)
tkinter.Label(login_frame, text="Username", font=('Arial', 15)).pack()
enteruser = tkinter.Entry(login_frame, width=30, font=(15))
enteruser.pack(pady=10, padx=50)

tkinter.Label(login_frame, text="Password", font=('Arial', 15)).pack()
enterpass = tkinter.Entry(login_frame, width=30, font=(15), show="*")
enterpass.pack(pady=10)

tkinter.Button(login_frame, text="Login", command=login_action, width=15, font=(15)).pack(pady=20)
tkinter.Button(login_frame, text="Create Account", command=show_signup_screen).pack(pady=10)

#SIGNUP SCREEN FRAME 
signup_frame = tkinter.Frame(base, bg='white', bd=2, )

tkinter.Label(signup_frame, text="SIGN UP", font=('Arial', 35, 'bold') ).pack(pady=20)
tkinter.Label(signup_frame, text="New Username", font=('Arial', 15)).pack()
signup_user = tkinter.Entry(signup_frame, width=30, font=(15))
signup_user.pack(pady=10, padx=50)

tkinter.Label(signup_frame, text="New Password", font=('Arial', 15)).pack()
signup_pass = tkinter.Entry(signup_frame, width=30, font=(15), show="*")
signup_pass.pack(pady=10)



tkinter.Button(signup_frame, text="Register", command=signup, width=15, font=(15)).pack(pady=20)
tkinter.Button(signup_frame, text="Back to Login", command=show_login_screen ).pack(pady=10)


show_login_screen()

base.mainloop()