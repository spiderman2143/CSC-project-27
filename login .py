import mysql.connector as psq
import tkinter 
from tkinter import messagebox
import PIL
# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '2101',
    'database': 'sandhya'
}

def init_db():
    """Creates the table if it doesn't exist."""
    con = psq.connect(**db_config)
    cur = con.cursor()
    # Fixed syntax: added 'S' to EXISTS and closed the parenthesis
    cur.execute("CREATE TABLE IF NOT EXISTS login (username VARCHAR(30) PRIMARY KEY, password VARCHAR(30))")
    con.commit()
    con.close()
#SIGNING UP BOX
def signup():
    username = enteruser.get()
    password = enterpass.get()
    #CHECKS IF EMPTY
    if not username or not password:
        messagebox.showwarning("Error", "Fields cannot be empty")
        return
    #INSERTING VALUES
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("INSERT INTO login (username, password) VALUES (%s, %s)",(username,password))
        con.commit()
        con.close()
        messagebox.showinfo("Success", f"Account created for {username}")
    #USERNAME ALREADY EXISTS
    except psq.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
#CHECKS IF SIGNUP U,P IS EQUAL TO LOGIN U,P
def checklogin(username, password):
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
    s = cur.fetchone()
    con.close()
    return s
#LOGIN BOX
def login_action():
    user = enteruser.get()
    pw = enterpass.get()
    #AFTER GETTING LOGIN CALLS CHECKLOGIN-WHICH CHECKS UP SAME-DISPLAYS MSG
    if checklogin(user, pw):
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Failed", "Invalid Username or Password")

# Initialize DB on startup
init_db()

# UI Setup
base = tkinter.Tk()
base.title("Secure Login")
base.geometry("1920x1080")
from PIL import Image, ImageTk
bg_image = Image.open("MOVIE.jpeg")
bg_image = bg_image.resize((1500, 1000))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tkinter.Label(base, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo

tkinter.Label(base, text="Username",width=30,font=('Arial',30),fg='navy').pack(pady=(100, 0))
enteruser = tkinter.Entry(base,width=50,font=(30),bg='white')
enteruser.pack()

tkinter.Label(base, text="Password",width=30,font=('Arial',30),fg='red').pack(pady=(30, 0))
enterpass = tkinter.Entry(base,width=50,font=(30),bg='white', show="*") # Hides password characters
enterpass.pack()

tkinter.Button(base, text="Login", command=login_action, width=70,font=(20),bg='grey').pack(pady=20)



base.mainloop()