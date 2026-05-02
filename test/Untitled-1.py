import mysql.connector as psq
import mysql.connector as psq
con=psq.connect(host='localhost',user='root',password='charan',database='sandhya')
cur=con.cursor()
def loginpg():
    cur.execute("create table if not exist login(username varchar(30) primary key,password varchar(20) not null;")
    con.commit()
    con.close()
loginpg()

def signup():
    username=enteruser.get()
    password=enterpass.get()
    con=psq.connect(host='localhost',user='root',password='charan',database='sandhya')
    cur=con.cursor()
    cur.execute(f"INSERT INTO login (username, password) VALUES ('{username}', '{password}')")
    con.commit()
    con.close()
    messagebox.showinfo("Success", f"Account created for {username}")
def checklogin(username,password):
    con=psq.connect(host='localhost',user='root',password='charan',database='sandhya')
    cur=con.cursor()
    cur.execute(f"SELECT * FROM login WHERE username = '{username}' AND password = '{password}' ")
    s=cur.fetchone()
    con.close()
    return s
print(checklogin("vc","123"))

import tkinter 
from tkinter import messagebox

def login_action():
    user = enteruser.get()
    password = enterpass.get()
    
    if checklogin(user, password):
        messagebox.showinfo("Nice", "Login done")
    else:
        messagebox.showerror("wrong", "Invalid Username/Password")

base = tkinter.Tk()

tkinter.Label(base, text="Username").pack(pady=(5,5),padx=(50,50))
enteruser = tkinter.Entry(base)
enteruser.pack()

tkinter.Label(base, text="Password").pack(pady=(10, 0))
enterpass= tkinter.Entry(base) 
enterpass.pack()




"""tkinter.Label(base,text="Email").pack(pady=(4,3))
enteremail=tkinter.Entry(base)
enteremail.pack()"""

tkinter.Button(base, text="Login", command=login_action).pack(pady=20)
tkinter.Button(base, text="Signup", command=loginpg).pack(pady=5)




