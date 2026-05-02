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
        query = "INSERT INTO login (username, password) VALUES (%s, %s)"
        cur.execute(query,(username,password))
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
    query = "SELECT * FROM login WHERE username = %s AND password = %s"
    cur.execute(query, (username, password))
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
base.geometry("300x300")
from PIL import Image, ImageTk
bg_image = Image.open("MOVIE.jpeg")
bg_image = bg_image.resize((300, 300))

bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tkinter.Label(base, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

bg_label.image = bg_photo

tkinter.Label(base, text="Username").pack(pady=(20, 0))
enteruser = tkinter.Entry(base)
enteruser.pack()

tkinter.Label(base, text="Password").pack(pady=(10, 0))
enterpass = tkinter.Entry(base, show="*") # Hides password characters
enterpass.pack()

tkinter.Button(base, text="Login", command=login_action, width=15).pack(pady=20)
tkinter.Button(base, text="Signup", command=signup, width=15).pack(pady=5)


base.mainloop()