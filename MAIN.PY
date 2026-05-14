import mysql.connector as psq
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import requests

# ---------------- CONFIGURATION ----------------
TMDB_API_KEY = "28e5e0639713f8c0e151cd61ed9f8f9a"  # Ensure this is your valid TMDb API key

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'charan',
    'database': 'sandhya'
}

current_user = None

# ---------------- DATABASE INITIALIZATION ----------------
def init_db():
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS userdetails (fullname VARCHAR(30) NOT NULL, age INT, gender VARCHAR(10), email VARCHAR(50), username VARCHAR(50) PRIMARY KEY, password VARCHAR(20), bio VARCHAR(50))")
    cur.execute("CREATE TABLE IF NOT EXISTS admindetails (username VARCHAR(50) PRIMARY KEY, password VARCHAR(20))")
    cur.execute("CREATE TABLE IF NOT EXISTS usergenres (username VARCHAR(50) PRIMARY KEY, genre1 VARCHAR(20), genre2 VARCHAR(20), genre3 VARCHAR(20))")
    
    # The reviews table has been completely removed.
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

# ---------------- ADMIN LOGIN ----------------
def checkadmin(username, password):
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("SELECT * FROM admindetails WHERE username=%s AND password=%s", (username, password))
    result = cur.fetchone()
    con.close()
    return result

def ADlogin_action():
    user = admin_user.get()
    pw = admin_pass.get()
    if not all([user,pw]):
        messagebox.showerror("Error", "All fields required")
        return
    if len(pw) <= 4:
        messagebox.showerror("Error", "Password must be > 4 characters")
        return
    
    if checkadmin(user, pw):
        messagebox.showinfo("Success", "Admin Login successful!")
    else:
        messagebox.showerror("Failed", "Invalid Admin Credentials")

# ---------------- USER LOGIN ----------------
def checklogin(username, password):
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("SELECT * FROM userdetails WHERE username=%s AND password=%s", (username, password))
    result = cur.fetchone()
    con.close()
    return result

def checkiffirsttime(username):
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("SELECT * FROM usergenres WHERE username=%s", (username,))
    result = cur.fetchone()
    con.close()
    
    return result is None

def login_action():
    global current_user 
    user = enteruser.get()
    pw = enterpass.get()
    
    if not all([user,pw]):
        messagebox.showerror("Error", "All fields required")
        return
    if len(pw) <= 4:
        messagebox.showerror("Error", "Password must be > 4 characters")
        return

    if checklogin(user, pw):
        current_user = user 
        if checkiffirsttime(user):
            show_genre_screen()    
        else:
            show_dashboard_screen() 
    else:
        messagebox.showerror("Failed", "Invalid Username or Password")

# ---------------- UI SETUP ----------------
base = tk.Tk()
base.title("Movie Discovery Platform")
base.geometry("1200x800")

try:
    img = Image.open("MOVIE.jpeg")
    img = img.resize((1200, 800))
    bg_photo = ImageTk.PhotoImage(img)
    bg_label = tk.Label(base, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

# ---------------- FRAME SWITCH ----------------
def show_signup_screen():
    login_frame.place_forget()
    genre_frame.place_forget()
    dashboard_frame.place_forget()
    admin_frame.place_forget()
    signup_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_login_screen():
    signup_frame.place_forget()
    genre_frame.place_forget()
    dashboard_frame.place_forget()
    admin_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_genre_screen():
    login_frame.place_forget()
    signup_frame.place_forget()
    dashboard_frame.place_forget()
    admin_frame.place_forget()
    genre_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_dashboard_screen():
    login_frame.place_forget()
    signup_frame.place_forget()
    genre_frame.place_forget()
    admin_frame.place_forget()
    dashboard_frame.place(relx=0.5, rely=0.5, anchor='center')
    
    welcome_label.config(text=f"Welcome back, {current_user}!")
    load_api_movies() # Fetch trending movies when entering dashboard

def show_adminscreen():
    login_frame.place_forget()
    signup_frame.place_forget()
    admin_frame.place(relx=0.5, rely=0.5, anchor='center')

# ---------------- LOGIN FRAME ----------------
login_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(login_frame, text="USER LOGIN", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)
tk.Label(login_frame, text="Username", font=('Arial', 15), bg='white').pack()
enteruser = tk.Entry(login_frame, width=30)
enteruser.pack(pady=10)
tk.Label(login_frame, text="Password", font=('Arial', 15), bg='white').pack()
enterpass = tk.Entry(login_frame, width=30, show="*")
enterpass.pack(pady=10)
tk.Button(login_frame, text="Login", command=login_action).pack(pady=20)
tk.Button(login_frame, text="Create Account", command=show_signup_screen).pack()
tk.Button(login_frame, text="Admin Login", command=show_adminscreen).pack(pady=5)

#---------------- ADMIN FRAME --------------
admin_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(admin_frame, text="ADMIN LOGIN", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)
tk.Label(admin_frame, text="Username", font=('Arial', 15), bg='white').pack()
admin_user = tk.Entry(admin_frame, width=30)
admin_user.pack(pady=10)
tk.Label(admin_frame, text="Password", font=('Arial', 15), bg='white').pack()
admin_pass = tk.Entry(admin_frame, width=30, show="*")
admin_pass.pack(pady=10)
tk.Button(admin_frame, text="Login", command=ADlogin_action).pack(pady=20)
tk.Button(admin_frame, text="Back", command=show_login_screen).pack()

# ---------------- SIGNUP FRAME ----------------
signup_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(signup_frame, text="SIGN UP", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)
tk.Label(signup_frame, text="Full Name", bg='white').pack()
name_entry = tk.Entry(signup_frame, width=30)
name_entry.pack()
tk.Label(signup_frame, text="Age", bg='white').pack()
age_entry = tk.Entry(signup_frame, width=30)
age_entry.pack()
tk.Label(signup_frame, text="Gender", bg='white').pack()

gender_var = tk.StringVar(value="Male")
frame = tk.Frame(signup_frame, bg='white')
frame.pack()
tk.Radiobutton(frame, text="Male", variable=gender_var, value="Male", bg='white').pack(side="left")
tk.Radiobutton(frame, text="Female", variable=gender_var, value="Female", bg='white').pack(side="left")
tk.Radiobutton(frame, text="Other", variable=gender_var, value="Other", bg='white').pack(side="left")

tk.Label(signup_frame, text="Email", bg='white').pack()
email_entry = tk.Entry(signup_frame, width=30)
email_entry.pack()
tk.Label(signup_frame, text="Bio", bg='white').pack()
bio_entry = tk.Entry(signup_frame, width=30)
bio_entry.pack()
tk.Label(signup_frame, text="Username", bg='white').pack()
user_entry = tk.Entry(signup_frame, width=30)
user_entry.pack()
tk.Label(signup_frame, text="Password", bg='white').pack()
pass_entry = tk.Entry(signup_frame, width=30, show="*")
pass_entry.pack()
tk.Label(signup_frame, text="Confirm Password", bg='white').pack()
confirm_entry = tk.Entry(signup_frame, width=30, show="*")
confirm_entry.pack()
tk.Button(signup_frame, text="Register", command=user_signup).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=show_login_screen).pack()

# ---------------- GENRE SELECTION FRAME ----------------
genre_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(genre_frame, text="SELECT GENRES", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)
tk.Label(genre_frame, text="Pick your top 3 favorite movie genres", font=('Arial', 15), bg='white').pack(pady=10)

movie_genres = ["Action", "Sci-Fi", "Comedy", "Drama", "Horror", "Thriller", "Romance", "Animation", "Documentary"]
genre_vars = {}

checkbox_container = tk.Frame(genre_frame, bg='white')
checkbox_container.pack(pady=10)

for genre in movie_genres:
    var = tk.IntVar()
    genre_vars[genre] = var
    chk = tk.Checkbutton(checkbox_container, text=genre, variable=var, bg='white', font=('Arial', 12))
    chk.pack(anchor='w', pady=2)

def submit_genres():
    selected_genres = []
    for genre_name, var in genre_vars.items():
        if var.get() == 1: 
            selected_genres.append(genre_name) 
    
    if len(selected_genres) != 3:
        messagebox.showerror("Error", "Please select exactly 3 genres")
    else:
        try:
            con = psq.connect(**db_config)
            cur = con.cursor()
            cur.execute(
                "INSERT INTO usergenres (username, genre1, genre2, genre3) VALUES (%s, %s, %s, %s)",
                (current_user, selected_genres[0], selected_genres[1], selected_genres[2])
            )
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Genres saved successfully!")
            show_dashboard_screen() 
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save genres: {e}")

tk.Button(genre_frame, text="Continue", command=submit_genres).pack(pady=20)

# ---------------- DASHBOARD & API INTEGRATION ----------------
dashboard_frame = tk.Frame(base, bg='white', bd=2, padx=40, pady=40)

welcome_label = tk.Label(dashboard_frame, text="Welcome to the Movie Platform!", font=('Arial', 24, 'bold'), bg='white')
welcome_label.pack(pady=10)

# Search Bar Area
search_frame = tk.Frame(dashboard_frame, bg='white')
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, width=40, font=('Arial', 12))
search_entry.pack(side=tk.LEFT, padx=10)

def trigger_search():
    query = search_entry.get().strip()
    load_api_movies(query)

tk.Button(search_frame, text="Search Movie", command=trigger_search).pack(side=tk.LEFT)
tk.Button(search_frame, text="Show Trending", command=trigger_search).pack(side=tk.LEFT, padx=10)

# Treeview to display movies
columns = ("ID", "Title", "Release Date", "Description")
movie_tree = ttk.Treeview(dashboard_frame, columns=columns, show="headings", height=12)
movie_tree.heading("ID", text="API ID")
movie_tree.heading("Title", text="Title")
movie_tree.heading("Release Date", text="Release Date")
movie_tree.heading("Description", text="Description")

movie_tree.column("ID", width=70)
movie_tree.column("Title", width=200)
movie_tree.column("Release Date", width=100)
movie_tree.column("Description", width=450)
movie_tree.pack(pady=10)

# Fetch movies directly from TMDb API
def load_api_movies(search_query=""):
    # Clear existing items
    for item in movie_tree.get_children():
        movie_tree.delete(item)
        


    # If search query is empty, get trending movies. Otherwise, search.
    if search_query == "":
        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    else:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={search_query}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results")
            
            # Display up to 20 results
            for movie in results[:20]:
                m_id = movie.get("id")
                title = movie.get("title")
                release = movie.get("release_date")
                
                # Clean up description (remove line breaks)
                desc = movie.get("overview", "No description available.").replace('\n', ' ')
                
                movie_tree.insert("", tk.END, values=(m_id, title, release, desc))
        else:
            pass
            
    except:
        pass

# ---------------- INITIALIZATION ----------------
init_db()
show_login_screen()

base.mainloop()