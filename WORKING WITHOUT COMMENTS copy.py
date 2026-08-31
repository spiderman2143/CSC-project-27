import mysql.connector as psq
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io  

# ---------------- CONFIGURATION ----------------
TMDB_API_KEY = "28e5e0639713f8c0e151cd61ed9f8f9a"  # Ensure this is your valid TMDb API key

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'charan123', 
    'database': 'charan'
}

current_user = None

# ---------------- DATABASE INITIALIZATION + TABLE CREATION----------------
def init_db():
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS userdetails (fullname VARCHAR(30) NOT NULL, age INT, gender VARCHAR(10), email VARCHAR(50), username VARCHAR(50) PRIMARY KEY, password VARCHAR(20), bio VARCHAR(50))")
        cur.execute("CREATE TABLE IF NOT EXISTS admindetails (username VARCHAR(50) PRIMARY KEY, password VARCHAR(20))")
        cur.execute("CREATE TABLE IF NOT EXISTS usergenres (username VARCHAR(50) PRIMARY KEY, genre1 VARCHAR(20), genre2 VARCHAR(20), genre3 VARCHAR(20))")
        cur.execute("CREATE TABLE IF NOT EXISTS reviews(review_id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50),movie_name VARCHAR(100),"
                    "story INT,screenplay INT,acting INT,direction INT,music INT,visual_effects INT,entertainment INT,avg_rating FLOAT)")
        # --- NEW WATCHLIST TABLE ---
        cur.execute("CREATE TABLE IF NOT EXISTS watchlist (username VARCHAR(50), movie_id INT, movie_name VARCHAR(100), poster_path VARCHAR(200))")
        con.commit()
        con.close()
    except Exception as e:
        print(f"DATABASE WARNING: Could not connect to MySQL. Error: {e}")

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
    
    #EMPTY FIELDS CHECK
    if not all([name, age, email, username, password, confirm]):
        messagebox.showerror("Error", "All fields required")
        return
    #AGE DIGIT CHECK
    if not age.isdigit():
        messagebox.showerror("Error", "Age must be a number")
        return
    #LENGTH OF PWD>4 CHECK
    if len(password) <= 4:
        messagebox.showerror("Error", "Password must be > 4 characters")
        return
    #CONFIRM PWD CHECK
    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match")
        return
        
    #INSERTING INTO SQL TABLE    
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("INSERT INTO userdetails (fullname, age, gender, email, username, password, bio) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (name, age, gender, email, username, password, bio))
        con.commit()
        con.close()

        messagebox.showinfo("Success", "Account created!")
        show_login_screen()

    except psq.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")

# ---------------- ADMIN LOGIN ----------------
def checkadmin(username, password):
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("SELECT * FROM admindetails WHERE username=%s AND password=%s", (username, password))
        result = cur.fetchone()
        con.close()
        return result 
    except:
        return None

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
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("SELECT * FROM userdetails WHERE username=%s AND password=%s", (username, password))
        result = cur.fetchone()
        con.close()
        return result
    except:
        return None

def checkiffirsttime(username):
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("SELECT * FROM usergenres WHERE username=%s", (username,))
        result = cur.fetchone()
        con.close()
        return result
    except:
        return None

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
            show_dashboard_screen()    
        else:
            show_genre_screen()  
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

# CREATE ALL FRAMES 
login_frame = tk.Frame(base, bg='white', bd=2)
admin_frame = tk.Frame(base, bg='white', bd=2)
signup_frame = tk.Frame(base, bg='white', bd=2)
genre_frame = tk.Frame(base, bg='white', bd=2)
dashboard_frame = tk.Frame(base, bg='white', bd=2, padx=40, pady=40)
profile_frame = tk.Frame(base, bg='white', bd=2)
watchlist_frame = tk.Frame(base, bg='white', bd=2) # NEW FRAME

# ---------------- FRAME SWITCHING HELPER ----------------
def hide_all_frames():
    login_frame.place_forget()
    admin_frame.place_forget()
    signup_frame.place_forget()
    genre_frame.place_forget()
    dashboard_frame.place_forget()
    profile_frame.place_forget()
    watchlist_frame.place_forget()

def show_signup_screen():
    hide_all_frames()
    signup_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_login_screen():
    hide_all_frames()
    login_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_adminscreen():
    hide_all_frames()
    admin_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_genre_screen():
    hide_all_frames()
    genre_frame.place(relx=0.5, rely=0.5, anchor='center')

def show_dashboard_screen():
    hide_all_frames()
    dashboard_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.9)
    welcome_label.config(text=f"Welcome back, {current_user}!")
    load_api_movies() 

# ---------------- LOGIN FRAME ----------------
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
tk.Label(admin_frame, text="ADMIN LOGIN", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)
tk.Label(admin_frame, text="Username", font=('Arial', 15), bg='white').pack()
admin_user = tk.Entry(admin_frame, width=30)
admin_user.pack(pady=10)
tk.Label(admin_frame, text="Password", font=('Arial', 15), bg='white').pack()
admin_pass = tk.Entry(admin_frame, width=30, show="*")
admin_pass.pack(pady=10)

tk.Button(admin_frame, text="Login", command=ADlogin_action).pack(pady=20)
tk.Button(admin_frame, text="Back to Login", command=show_login_screen).pack()

# ---------------- SIGNUP FRAME ----------------
tk.Label(signup_frame, text="SIGN UP", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)

tk.Label(signup_frame, text="Full Name", bg='white').pack()
name_entry = tk.Entry(signup_frame, width=30)
name_entry.pack()

tk.Label(signup_frame, text="Age", bg='white').pack()
age_entry = tk.Entry(signup_frame, width=30)
age_entry.pack()

tk.Label(signup_frame, text="Gender", bg='white').pack()
gender_var = tk.StringVar(value="Male")
frame_g = tk.Frame(signup_frame, bg='white')
frame_g.pack()
tk.Radiobutton(frame_g, text="Male", variable=gender_var, value="Male", bg='white').pack(side="left")
tk.Radiobutton(frame_g, text="Female", variable=gender_var, value="Female", bg='white').pack(side="left")
tk.Radiobutton(frame_g, text="Other", variable=gender_var, value="Other", bg='white').pack(side="left")

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
    for genre_name in genre_vars:
        if genre_vars[genre_name].get() == 1: 
            selected_genres.append(genre_name) 
            
    if len(selected_genres) != 3:
        messagebox.showerror("Error", "Please select exactly 3 genres")
    else:
        try:
            con = psq.connect(**db_config)
            cur = con.cursor()
            cur.execute("INSERT INTO usergenres (username, genre1, genre2, genre3) VALUES (%s, %s, %s, %s)",
                (current_user, selected_genres[0], selected_genres[1], selected_genres[2]))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Genres saved successfully!")
            show_dashboard_screen() 
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save genres: {e}")

tk.Button(genre_frame, text="Continue", command=submit_genres).pack(pady=20)


# ---------------- WATCHLIST SYSTEM ----------------
def add_to_watchlist(movie):
    movie_id = movie.get("id")
    title = movie.get("title")
    poster = movie.get("poster_path")

    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        
        # Check if already added
        cur.execute("SELECT * FROM watchlist WHERE username=%s AND movie_id=%s", (current_user, movie_id))
        if cur.fetchone():
            messagebox.showinfo("Info", f"'{title}' is already in your Watchlist!")
        else:
            cur.execute("INSERT INTO watchlist (username, movie_id, movie_name, poster_path) VALUES (%s, %s, %s, %s)",
                        (current_user, movie_id, title, poster))
            con.commit()
            messagebox.showinfo("Success", f"Added '{title}' to Watchlist!")
        con.close()
    except Exception as e:
        messagebox.showerror("Error", f"Could not add to watchlist: {e}")

def remove_from_watchlist(movie_id):
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("DELETE FROM watchlist WHERE username=%s AND movie_id=%s", (current_user, movie_id))
        con.commit()
        con.close()
        messagebox.showinfo("Success", "Removed from Watchlist")
        show_watchlist_screen() # Refresh the screen
    except Exception as e:
        messagebox.showerror("Error", f"Could not remove movie: {e}")

def show_watchlist_screen():
    hide_all_frames()
    watchlist_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.9)

    for widget in watchlist_frame.winfo_children():
        widget.destroy()

    tk.Label(watchlist_frame, text="📺 MY WATCHLIST", font=('Arial', 24, 'bold'), bg='white').pack(pady=10)
    tk.Button(watchlist_frame, text="Back to Dashboard", font=('Arial', 12, 'bold'), bg='black', fg='white', command=show_dashboard_screen).pack(pady=5)

    # Scrollable Canvas setup for Watchlist
    wl_canvas_frame = tk.Frame(watchlist_frame, bg='white')
    wl_canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    wl_canvas = tk.Canvas(wl_canvas_frame, bg='white')
    wl_scrollbar = ttk.Scrollbar(wl_canvas_frame, orient="vertical", command=wl_canvas.yview)
    wl_scrollable_frame = tk.Frame(wl_canvas, bg='white')
    
    wl_canvas.create_window((0, 0), window=wl_scrollable_frame, anchor="nw") 
    wl_canvas.configure(yscrollcommand=wl_scrollbar.set)
    wl_canvas.pack(side="left", fill="both", expand=True)
    wl_scrollbar.pack(side="right", fill="y") 

    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("SELECT movie_id, movie_name, poster_path FROM watchlist WHERE username=%s", (current_user,))
        saved_movies = cur.fetchall()
        con.close()

        if not saved_movies:
            tk.Label(wl_scrollable_frame, text="Your watchlist is empty.", font=('Arial', 14), bg='white').pack(pady=40, padx=40)
            return

        row, col, max_columns = 0, 0, 4
        for movie_id, title, poster_path in saved_movies:
            movie_card = tk.Frame(wl_scrollable_frame, bg='white', bd=1, relief="solid")
            movie_card.grid(row=row, column=col, padx=15, pady=15)

            if poster_path:
                img_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
                try:
                    img_response = requests.get(img_url)
                    img_data = Image.open(io.BytesIO(img_response.content)).resize((150, 225))
                    photo = ImageTk.PhotoImage(img_data)
                    img_label = tk.Label(movie_card, image=photo, bg='white')
                    img_label.image = photo 
                    img_label.pack(pady=5, padx=5)
                except:
                    pass

            display_title = title[:19] + "..." if len(title) > 22 else title
            tk.Label(movie_card, text=display_title, font=('Arial', 10, 'bold'), bg='white').pack(pady=(0, 5))
            
            tk.Button(movie_card, text="Remove", bg='red', fg='white', command=lambda m_id=movie_id: remove_from_watchlist(m_id)).pack(pady=10)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1

        wl_scrollable_frame.update_idletasks()
        wl_canvas.configure(scrollregion=wl_canvas.bbox("all"))

    except Exception as e:
        tk.Label(wl_scrollable_frame, text=f"Error loading watchlist: {e}", bg='white').pack()


# ---------------- DASHBOARD ----------------
welcome_label = tk.Label(dashboard_frame, text="Welcome to the Movie Platform!", font=('Arial', 24, 'bold'), bg='white')
welcome_label.pack(pady=10)

# Dashboard Navbar Buttons
profile_btn = tk.Button(dashboard_frame,text="👤 Profile",font=('Arial', 11, 'bold'),bg='black',fg='white',cursor='hand2',command=lambda: show_profile_screen())
profile_btn.place(relx=0.95, rely=0.02, anchor='ne')

watchlist_btn = tk.Button(dashboard_frame,text="📺 Watchlist",font=('Arial', 11, 'bold'),bg='green',fg='white',cursor='hand2',command=show_watchlist_screen)
watchlist_btn.place(relx=0.85, rely=0.02, anchor='ne')

search_frame = tk.Frame(dashboard_frame, bg='white')
search_frame.pack(pady=10)
search_entry = tk.Entry(search_frame, width=40, font=('Arial', 12))
search_entry.pack(side=tk.LEFT, padx=10)

def trigger_search():
    query = search_entry.get().strip()
    load_api_movies(query)

def show_trending():
    search_entry.delete(0, tk.END)
    load_api_movies("")

tmdb_genre_ids = {"Action": 28,"Sci-Fi": 878,"Comedy": 35,"Drama": 18,"Horror": 27,"Thriller": 53,"Romance": 10749,"Animation": 16,"Documentary": 99}

def show_recommendations():
    for widget in scrollable_movie_frame.winfo_children():
        widget.destroy()
    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("SELECT genre1, genre2, genre3 FROM usergenres WHERE username=%s",(current_user,))
        genres = cur.fetchone()
        
        if not genres:
            return
            
        genres = list(genres)
        con.close()

        genre_ids = []
        for genre in genres: 
            genre_ids.append(str(tmdb_genre_ids[genre])) 

        genre_string = ",".join(genre_ids)
        url = (f"https://api.themoviedb.org/3/discover/movie?"f"api_key={TMDB_API_KEY}"f"&with_genres={genre_string}")
        response = requests.get(url)

        if response.status_code == 200: 
            data = response.json() 
            results = data.get("results") 

            row, col, max_columns = 0, 0, 4
            for movie in results[:10]:
                title = movie.get("title")
                poster_path = movie.get("poster_path")

                movie_card = tk.Frame(scrollable_movie_frame,bg='white',bd=1,relief="solid")
                movie_card.grid(row=row,column=col,padx=15,pady=15)

                if poster_path:
                    img_url = f"https://image.tmdb.org/t/p/w200{poster_path}" 
                    try:
                        img_response = requests.get(img_url)
                        img_data = img_response.content 
                        img_data = Image.open(io.BytesIO(img_data))
                        img_data = img_data.resize((150, 225)) 
                        photo = ImageTk.PhotoImage(img_data) 

                        img_label = tk.Label(movie_card,image=photo,bg='white')
                        img_label.image = photo 
                        img_label.pack(pady=5, padx=5)
                    except:
                        pass

                if len(title) > 22:
                    title = title[:19] + "..."

                tk.Label(movie_card,text=title,font=('Arial', 10, 'bold'),bg='white').pack(pady=(0,5))
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1

                tk.Button(movie_card,text="Add Review",bg='black',fg='white',cursor='hand2',command=lambda m=movie: open_review_window(m)).pack(pady=2)
                tk.Button(movie_card, text="See Details", bg='blue', fg='white', command=lambda m=movie: open_details_window(m)).pack(pady=2)
                tk.Button(movie_card, text="+ Watchlist", bg='green', fg='white', command=lambda m=movie: add_to_watchlist(m)).pack(pady=2)

    except Exception as e:
        pass

    scrollable_movie_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

tk.Button(search_frame, text="Search Movie", command=trigger_search).pack(side=tk.LEFT)
tk.Button(search_frame, text="Show Trending", command=show_trending).pack(side=tk.LEFT, padx=10)
tk.Button(search_frame,text="Recommended For You",bg='darkblue',fg='white',command=show_recommendations).pack(side=tk.LEFT, padx=10)

# ------SCROLLBAR SETUP---------
canvas_frame = tk.Frame(dashboard_frame, bg='white')
canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

canvas = tk.Canvas(canvas_frame, bg='white')
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollable_movie_frame = tk.Frame(canvas, bg='white')

canvas.create_window((0, 0), window=scrollable_movie_frame, anchor="nw") 
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y") 

#-------------REVIEW SYSTEM-----------------------
def open_review_window(movie):
    movie_name = movie.get("title")
    review_win = tk.Toplevel(base)
    review_win.title("Movie Review")
    review_win.geometry("500x700")
    review_win.config(bg='white')

    tk.Label(review_win,text=movie_name,font=('Arial', 20, 'bold'),bg='white').pack(pady=20)
    parameters = ["Story","Screenplay","Acting","Direction","Music","Visual Effects","Entertainment"]
    
    rating_vars = {}
    for param in parameters:
        tk.Label(review_win,text=param,font=('Arial', 14),bg='white').pack() 
        var = tk.IntVar()
        rating_vars[param] = var 

        star_frame = tk.Frame(review_win,bg='#1e1e1e',padx=10,pady=5)
        star_frame.pack(pady=5)
        for i in range(1, 6):
            tk.Radiobutton(star_frame,text="★",variable=var,value=i,indicatoron=0,width=3,font=('Arial', 14),bg='gold').pack(side='left', padx=2)

    def save_review():
        story = rating_vars["Story"].get()
        screenplay = rating_vars["Screenplay"].get()
        acting = rating_vars["Acting"].get()
        direction = rating_vars["Direction"].get()
        music = rating_vars["Music"].get()
        visual = rating_vars["Visual Effects"].get()
        entertainment = rating_vars["Entertainment"].get()
        total = story + screenplay + acting + direction + music + visual + entertainment
        avg = total / 7

        try:
            con = psq.connect(**db_config)
            cur = con.cursor()
            cur.execute("INSERT INTO reviews(username,movie_name,story,screenplay,acting,direction,music,visual_effects,entertainment,avg_rating)"
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(current_user,movie_name,story,screenplay,acting,direction,music,visual,entertainment,avg))
            con.commit()
            con.close()

            messagebox.showinfo("Success",f"Review Saved!\nAverage Rating: {round(avg,1)} ★")
            review_win.destroy()
        except:
            pass

    tk.Button(review_win,text="Submit Review",font=('Arial', 14, 'bold'),bg='red',fg='white',command=save_review).pack(pady=20)

#-------------MOVIE DETAILS SYSTEM-----------------------
def open_details_window(movie):
    title = movie.get("title")
    overview = movie.get("overview" )
    release_date = movie.get("release_date" )
    
    details_win = tk.Toplevel(base)
    details_win.title(f"{title} - Details")
    details_win.geometry("600x400")
    details_win.config(bg='white')
    
    tk.Label(details_win, text=title, font=('Arial', 20, 'bold'), bg='white', wraplength=550).pack(pady=15)
    info_frame = tk.Frame(details_win, bg='white')
    info_frame.pack(pady=5)
    tk.Label(info_frame, text=f"Release Date: {release_date}", font=('Arial', 12, 'bold'), bg='white').pack(side=tk.LEFT, padx=20)
    
    tk.Label(details_win, text="Synopsis:", font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 5))
    tk.Message(details_win, text=overview, font=('Arial', 12), bg='white', width=550, justify=tk.CENTER).pack(pady=5)
    tk.Button(details_win, text="Close", font=('Arial', 12, 'bold'), bg='red', fg='white', command=details_win.destroy).pack(pady=20)

# FETCH MOVIE AND DISPLAY IN GRID
def load_api_movies(search_query=""):
    for widget in scrollable_movie_frame.winfo_children():
        widget.destroy()

    if search_query == "": 
        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    else: 
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={search_query}"

    try:
        response = requests.get(url)
        if response.status_code == 200: 
            data = response.json() 
            results = data.get("results") 
            row = 0
            col = 0
            max_columns = 4 

            for movie in results[:10]: 
                title = movie.get("title")
                poster_path = movie.get("poster_path") 
                
                movie_card = tk.Frame(scrollable_movie_frame, bg='white', bd=1, relief="solid")
                movie_card.grid(row=row, column=col, padx=15, pady=15)
                
                if poster_path:
                    img_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
                    try:
                        img_response = requests.get(img_url) 
                        img_data = img_response.content 
                        img_data = Image.open(io.BytesIO(img_data)) 
                        img_data = img_data.resize((150, 225)) 
                        photo = ImageTk.PhotoImage(img_data) 
                        img_label = tk.Label(movie_card, image=photo, bg='white')
                        img_label.image = photo 
                        img_label.pack(pady=5, padx=5)
                    except:
                        pass

                if len(title) > 22 :
                    title = title[:19] + "..."

                tk.Label(movie_card, text=title, font=('Arial', 10, 'bold'), bg='white').pack(pady=(0, 5))
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
                
                tk.Button(movie_card, text="See Details", bg='blue', fg='white', command=lambda m=movie: open_details_window(m)).pack(pady=2)
                tk.Button(movie_card,text="Add Review",bg='black',fg='white',command=lambda m=movie: open_review_window(m)).pack(pady=2)
                tk.Button(movie_card, text="+ Watchlist", bg='green', fg='white', command=lambda m=movie: add_to_watchlist(m)).pack(pady=2)
                    
    except :
        pass

    scrollable_movie_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

#----------------------USER PROFILE (SINGLE SCREEN)--------------------------------------
def show_profile_screen():
    hide_all_frames()
    profile_frame.place(relx=0.5, rely=0.5, anchor='center')

    for widget in profile_frame.winfo_children():
        widget.destroy()

    try:
        con = psq.connect(**db_config)
        cur = con.cursor()
        cur.execute("SELECT * FROM userdetails WHERE username=%s",(current_user,))
        user_data = cur.fetchone() 
        cur.execute("SELECT genre1, genre2, genre3 FROM usergenres WHERE username=%s",(current_user,))
        genre_data = cur.fetchone() 
        con.close()
        
        if not user_data or not genre_data:
            return

        fullname, age, gender, email, username, password, bio = user_data
        genre1, genre2, genre3 = genre_data

        tk.Label(profile_frame,text="👤 USER PROFILE",font=('Arial', 24, 'bold'),bg='white',fg='black').pack(pady=20)
        info_frame = tk.Frame(profile_frame,bg='lightgrey',bd=2,relief='solid',padx=20,pady=20)
        info_frame.pack(pady=10, padx=20, fill='both', expand=True)

        tk.Label(info_frame,text=f"Full Name : {fullname}",font=('Arial', 14),bg='lightgrey',anchor='w').pack(fill='x', pady=8)
        tk.Label(info_frame,text=f"Age : {age}",font=('Arial', 14),bg='lightgrey',anchor='w').pack(fill='x', pady=8)
        tk.Label(info_frame,text=f"Gender : {gender}",font=('Arial', 14),bg='lightgrey',anchor='w').pack(fill='x', pady=8)
        tk.Label(info_frame,text=f"Email : {email}",font=('Arial', 14),bg='lightgrey',anchor='w').pack(fill='x', pady=8)
        tk.Label(info_frame,text=f"Username : {username}",font=('Arial', 14),bg='lightgrey',anchor='w').pack(fill='x', pady=8)
        tk.Label(info_frame,text=f"Password : {password}",font=('Arial', 14),bg='lightgrey',anchor='w').pack(fill='x', pady=8)
        tk.Label(info_frame,text=f"Bio : {bio}",font=('Arial', 14),bg='lightgrey',anchor='w',wraplength=350,justify='left').pack(fill='x', pady=8)

        tk.Label(info_frame,text="Favorite Genres",font=('Arial', 16, 'bold'),bg='lightgrey').pack(pady=15)
        tk.Label(info_frame,text=f"• {genre1}",font=('Arial', 13),bg='lightgrey').pack(pady=2)
        tk.Label(info_frame,text=f"• {genre2}",font=('Arial', 13),bg='lightgrey').pack(pady=2)
        tk.Label(info_frame,text=f"• {genre3}",font=('Arial', 13),bg='lightgrey').pack(pady=2)

        tk.Button(profile_frame,text="Back to Dashboard",font=('Arial', 12, 'bold'),bg='black',fg='white',command=show_dashboard_screen).pack(pady=20)
    
    except Exception as e:
        tk.Label(profile_frame, text=f"Error loading profile: {e}", fg="red", bg="white").pack(pady=20)
        tk.Button(profile_frame,text="Back to Dashboard",font=('Arial', 12, 'bold'),bg='black',fg='white',command=show_dashboard_screen).pack(pady=20)

# ---------------- INITIALIZATION ----------------
init_db()
show_login_screen()
base.mainloop()