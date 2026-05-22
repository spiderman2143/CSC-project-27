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
    'password': '2101', 
    'database': 'sandhya'
}

current_user = None

# ---------------- DATABASE INITIALIZATION + TABLE CREATION----------------
def init_db():
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS userdetails (fullname VARCHAR(30) NOT NULL, age INT, gender VARCHAR(10), email VARCHAR(50), username VARCHAR(50) PRIMARY KEY, password VARCHAR(20), bio VARCHAR(50))")
    cur.execute("CREATE TABLE IF NOT EXISTS admindetails (username VARCHAR(50) PRIMARY KEY, password VARCHAR(20))")
    cur.execute("CREATE TABLE IF NOT EXISTS usergenres (username VARCHAR(50) PRIMARY KEY, genre1 VARCHAR(20), genre2 VARCHAR(20), genre3 VARCHAR(20))")
    cur.execute("CREATE TABLE IF NOT EXISTS reviews(review_id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50),movie_name VARCHAR(100),"
"story INT,screenplay INT,acting INT,direction INT,music INT,visual_effects INT,entertainment INT,avg_rating FLOAT)")
    con.commit()
    con.close()

# ---------------- SIGNUP ----------------
#FACILITATES SIGNUP PROCESS
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
    if len(password)<= 4:
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

# ---------------- ADMIN LOGIN ----------------
#CHECKS DATA FROM SQL TABLE
def checkadmin(username, password):
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("SELECT * FROM admindetails WHERE username=%s AND password=%s", (username, password))
    result = cur.fetchone()
    con.close()
    return result 

#FACILITATES ADMINLOGIN PROCESS
def ADlogin_action():
    user = admin_user.get()
    pw = admin_pass.get()
    #EMPTY FIELD CHECK
    if not all([user,pw]):
        messagebox.showerror("Error", "All fields required")
        return
    #LENGTH OF PWD>4 CHECK
    if len(pw)<= 4:
        messagebox.showerror("Error", "Password must be > 4 characters")
        return
    
    if checkadmin(user, pw):
        messagebox.showinfo("Success", "Admin Login successful!")
    else:
        messagebox.showerror("Failed", "Invalid Admin Credentials")

# ---------------- USER LOGIN ----------------
#CHECKS DATA FROM SQL TABLE
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
    return result

#FACILITATES USERLOGIN PROCESS
def login_action():
    global current_user 
    user = enteruser.get()
    pw = enterpass.get()
    #EMPTY FIELD CHECK
    if not all([user,pw]):
        messagebox.showerror("Error", "All fields required")
        return
    #LENGTH OF PWD>4 CHECK
    if len(pw) <= 4:
        messagebox.showerror("Error", "Password must be > 4 characters")
        return

    if checklogin(user, pw):
        current_user = user 
        if checkiffirsttime(user): #IF RESULT IS TRUE-GENRES ALREADY SELECTED-GO TO DASHBOARD
            show_dashboard_screen()    
        else:
            show_genre_screen()  #RESULT IS FALSE-GENRES NOT SELECTED-GO TO GENRE SCREEN
    else:
        messagebox.showerror("Failed", "Invalid Username or Password")

# ---------------- UI SETUP ----------------
base = tk.Tk()
base.title("Movie Discovery Platform")
base.geometry("1200x800")

#BACKGROUND PICTURE
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

def show_adminscreen():
    login_frame.place_forget()
    signup_frame.place_forget()
    genre_frame.place_forget()
    dashboard_frame.place_forget()
    admin_frame.place(relx=0.5, rely=0.5, anchor='center')

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
    load_api_movies() 

# ---------------- LOGIN FRAME ----------------
#FRAME CREATION AND TITLE
login_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(login_frame, text="USER LOGIN", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)

#USERNAME BOX
tk.Label(login_frame, text="Username", font=('Arial', 15), bg='white').pack()
enteruser = tk.Entry(login_frame, width=30)
enteruser.pack(pady=10)

#PASSWORD BOX
tk.Label(login_frame, text="Password", font=('Arial', 15), bg='white').pack()
enterpass = tk.Entry(login_frame, width=30, show="*")
enterpass.pack(pady=10)

#3 BUTTONS-LOGIN,SIGNUP,ADMIN
tk.Button(login_frame, text="Login", command=login_action).pack(pady=20)
tk.Button(login_frame, text="Create Account", command=show_signup_screen).pack()
tk.Button(login_frame, text="Admin Login", command=show_adminscreen).pack(pady=5)

#---------------- ADMIN FRAME --------------
#FRAME CREATION AND TITLE
admin_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(admin_frame, text="ADMIN LOGIN", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)

#USERNAME BOX
tk.Label(admin_frame, text="Username", font=('Arial', 15), bg='white').pack()
admin_user = tk.Entry(admin_frame, width=30)
admin_user.pack(pady=10)

#PASSWORD BOX
tk.Label(admin_frame, text="Password", font=('Arial', 15), bg='white').pack()
admin_pass = tk.Entry(admin_frame, width=30, show="*")
admin_pass.pack(pady=10)

#2 BUTTONS-LOGIN,BACK
tk.Button(admin_frame, text="Login", command=ADlogin_action).pack(pady=20)
tk.Button(admin_frame, text="Back to Login", command=show_login_screen).pack()

# ---------------- SIGNUP FRAME ----------------
#FRAME CREATION AND TITLE
signup_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(signup_frame, text="SIGN UP", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)

#FULLNAME BOX
tk.Label(signup_frame, text="Full Name", bg='white').pack()
name_entry = tk.Entry(signup_frame, width=30)
name_entry.pack()

#AGE BOX
tk.Label(signup_frame, text="Age", bg='white').pack()
age_entry = tk.Entry(signup_frame, width=30)
age_entry.pack()

#GENDER BOX
tk.Label(signup_frame, text="Gender", bg='white').pack()
gender_var = tk.StringVar(value="Male")
frame = tk.Frame(signup_frame, bg='white')
frame.pack()
tk.Radiobutton(frame, text="Male", variable=gender_var, value="Male", bg='white').pack(side="left")
tk.Radiobutton(frame, text="Female", variable=gender_var, value="Female", bg='white').pack(side="left")
tk.Radiobutton(frame, text="Other", variable=gender_var, value="Other", bg='white').pack(side="left")

#EMAIL BOX
tk.Label(signup_frame, text="Email", bg='white').pack()
email_entry = tk.Entry(signup_frame, width=30)
email_entry.pack()

#BIO BOX
tk.Label(signup_frame, text="Bio", bg='white').pack()
bio_entry = tk.Entry(signup_frame, width=30)
bio_entry.pack()

#USERNAME BOX
tk.Label(signup_frame, text="Username", bg='white').pack()
user_entry = tk.Entry(signup_frame, width=30)
user_entry.pack()

#PASSWORD BOX
tk.Label(signup_frame, text="Password", bg='white').pack()
pass_entry = tk.Entry(signup_frame, width=30, show="*")
pass_entry.pack()

#CONFIRM PASSWORD BOX
tk.Label(signup_frame, text="Confirm Password", bg='white').pack()
confirm_entry = tk.Entry(signup_frame, width=30, show="*")
confirm_entry.pack()

#2 BUTTONS-REGISTER,BACK
tk.Button(signup_frame, text="Register", command=user_signup).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=show_login_screen).pack()

# ---------------- GENRE SELECTION FRAME ----------------
#FRAME CREATION,TITLE,MESSAGE
genre_frame = tk.Frame(base, bg='white', bd=2)
tk.Label(genre_frame, text="SELECT GENRES", font=('Arial', 30, 'bold'), bg='white').pack(pady=20)
tk.Label(genre_frame, text="Pick your top 3 favorite movie genres", font=('Arial', 15), bg='white').pack(pady=10)

movie_genres = ["Action", "Sci-Fi", "Comedy", "Drama", "Horror", "Thriller", "Romance", "Animation", "Documentary"]
genre_vars = {} #STORES KEY:GENRES,VALUE:1 OR 0
checkbox_container = tk.Frame(genre_frame, bg='white')
checkbox_container.pack(pady=10)
for genre in movie_genres:
    var = tk.IntVar() #CONVERTS SELECTED BOX TO NUMBER-1 FOR SELECTED,0 FOR NOT SELECTED 
    genre_vars[genre] = var 
    chk = tk.Checkbutton(checkbox_container, text=genre, variable=var, bg='white', font=('Arial', 12))
    chk.pack(anchor='w', pady=2)

def submit_genres():
    selected_genres = [] #STORES 3 SELECTED GENRES
    for genre_name in genre_vars():
        if genre_vars[genre_name]==1: #IF VALUE IS 1,APPEND TO SELECTED GENRES
            selected_genres.append(genre_name) 
    # ONLY 3 GENRES CHECK
    if len(selected_genres) != 3:
        messagebox.showerror("Error", "Please select exactly 3 genres")
    else:
        #INSERT DATA INTO SQL TABLE
        try:
            con = psq.connect(**db_config)
            cur = con.cursor()
            cur.execute("INSERT INTO usergenres (username, genre1, genre2, genre3) VALUES (%s, %s, %s, %s)",
                (current_user, selected_genres[0], selected_genres[1], selected_genres[2]))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Genres saved successfully!")
            show_dashboard_screen() 
        except:
            pass

tk.Button(genre_frame, text="Continue", command=submit_genres).pack(pady=20)

# ---------------- DASHBOARD ----------------
dashboard_frame = tk.Frame(base, bg='white', bd=2, padx=40, pady=40)
welcome_label = tk.Label(dashboard_frame, text="Welcome to the Movie Platform!", font=('Arial', 24, 'bold'), bg='white')
welcome_label.pack(pady=10)

#---------------------SEARCH BAR-------------------
search_frame = tk.Frame(dashboard_frame, bg='white')
search_frame.pack(pady=10)
#SEARCH BOX
search_entry = tk.Entry(search_frame, width=40, font=('Arial', 12))
search_entry.pack(side=tk.LEFT, padx=10)

#TO SEARCH A PARTCULAR MOVIE-Search movie button
def trigger_search():
    query = search_entry.get().strip()
    load_api_movies(query)

#TO SHOW TRENDING MOVIES GENERAL-Show trending button
def show_trending():
    search_entry.delete(0, tk.END)
    load_api_movies("")

#TO SHOW RECOMMENDATION BASED ON SELECTED GENRES-Show recommendation button
tmdb_genre_ids = {"Action": 28,"Sci-Fi": 878,"Comedy": 35,"Drama": 18,"Horror": 27,"Thriller": 53,"Romance": 10749,"Animation": 16,"Documentary": 99}
def show_recommendations():
    #CLEAR OLD MOVIES
    for widget in scrollable_movie_frame.winfo_children():
        widget.destroy()
    try:
        #CONNECT DATABASE
        con = psq.connect(**db_config)
        cur = con.cursor()
        #FETCH USER GENRES
        cur.execute("SELECT genre1, genre2, genre3 FROM usergenres WHERE username=%s",(current_user,))
        genres = cur.fetchone() #TUPLE CONTAINING 3 GENRES
        genres=list(genres) #CONVERTING TO LIST
        con.close()

        #CONVERT GENRES TO TMDB IDS
        genre_ids = []
        for genre in genres: #ITERATING THRU LIST
                genre_ids.append(str(tmdb_genre_ids[genre])) #ADDING GENREID FOR PARTICULAR GENRE

        # JOIN IDS-FORMAT NEEDED FOR TMDB
        genre_string = ",".join(genre_ids)

        # TMDB DISCOVER API
        url = (f"https://api.themoviedb.org/3/discover/movie?"f"api_key={TMDB_API_KEY}"f"&with_genres={genre_string}")
        response = requests.get(url)

        if response.status_code == 200: #WHEN SITE RUNS AND GIVES OUTPUT-200 DEFAULT STATUS CODE
            data = response.json() #data IS DICT WITH KEY-REQUESTS AND ENTIRE MOVIE LIST-VALUE
            results = data.get("results") #results IS ENTIRE MOVIE LIST

            row = 0
            col = 0
            max_columns = 4 #1 LINE SHOULD CONTAIN ONLY 4 MOVIES
            for movie in results[:10]: #DISPLAY 10 MOVIES
                title = movie.get("title")
                poster_path = movie.get("poster_path") #PATH FROM API DATABASE

                movie_card = tk.Frame(scrollable_movie_frame,bg='white',bd=1,relief="solid")
                movie_card.grid(row=row,column=col,padx=15,pady=15)

                img_url = f"https://image.tmdb.org/t/p/w200{poster_path}" 

                try:
                    img_response = requests.get(img_url) #URL LINK
                    img_data = img_response.content #ACTUAL IMAGE CONTENT
                    img_data = Image.open(io.BytesIO(img_data)) #USING IO MODULE OPEN IMAGE(FILE HANDLER)
                    img_data = img_data.resize((150, 225)) #RESIZE TO FIT WINDOW
                    photo = ImageTk.PhotoImage(img_data) #FINAL

                    img_label = tk.Label(movie_card,image=photo,bg='white')
                    img_label.image = photo #VARIABLE TO STORE
                    img_label.pack(pady=5)

                except:
                        pass

                #TITLE CONDITION FOR BIG MOVIE NAMES
                if len(title) > 22:
                    title = title[:19] + "..."

                tk.Label(movie_card,text=title,font=('Arial', 10, 'bold'),bg='white').pack(pady=(0,5))
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1

                # REVIEW BUTTON
                tk.Button(movie_card,text="Add Review",bg='black',fg='white',cursor='hand2',command=lambda m=movie: open_review_window(m)).pack(pady=5)
                #SEE DETAILS BUTTON 
                tk.Button(movie_card, text="See Details", bg='blue', fg='white', command=lambda m=movie: open_details_window(m)).pack(pady=2)

    except Exception as e:
        pass

    scrollable_movie_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

#3 BUTTONS=SEARCHMOVIE,SHOWTRENDING,SHOWRECOMMENDATION
tk.Button(search_frame, text="Search Movie", command=trigger_search).pack(side=tk.LEFT)
tk.Button(search_frame, text="Show Trending", command=show_trending).pack(side=tk.LEFT, padx=10)
tk.Button(search_frame,text="Recommended For You",bg='darkblue',fg='white',command=show_recommendations).pack(side=tk.LEFT, padx=10)

# ------SCROLLBAR SETUP---------
#FRAME CREATION
canvas_frame = tk.Frame(dashboard_frame, bg='white')
canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

canvas = tk.Canvas(canvas_frame, bg='white')
scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)#SCROLL VERTICALLY(YVIEW)
scrollable_movie_frame = tk.Frame(canvas, bg='white')

canvas.create_window((0, 0), window=scrollable_movie_frame, anchor="nw") #AS WE SCROLL DOWN-FRAME GETS CREATED
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y") #TOWARDS THE EXTREME RIGHT OF PAGE

#-------------REVIEW SYSTEM-----------------------
def open_review_window(movie):
    movie_name = movie.get("title")
    #SIDE WINDOW review_win
    review_win = tk.Toplevel(base)
    review_win.title("Movie Review")
    review_win.geometry("500x700")
    review_win.config(bg='white')

    #MOVIE TITLE HEADING
    tk.Label(review_win,text=movie_name,font=('Arial', 20, 'bold'),bg='white').pack(pady=20)

    parameters = ["Story","Screenplay","Acting","Direction","Music","Visual Effects","Entertainment"]
    #DICTIONARY THAT HAS KEY:PARAMETERS,VALUE:RATING IN NUMBER
    rating_vars = {}
    for param in parameters:
        tk.Label(review_win,text=param,font=('Arial', 14),bg='white').pack() #DISPLAYS PARAMETER 
        var = tk.IntVar() #STORES STAR VALUE AS NUMBER
        rating_vars[param] = var 

        #STAR BULIDING
        star_frame = tk.Frame(review_win,bg='#1e1e1e',padx=10,pady=5)
        star_frame.pack(pady=5)
        for i in range(1, 6):
            #INSIDE STARFRAME,TEXT IS STAR,VARIABLE VAR(NUMBER STORAGE),i VALUE FOR EACH STAR,INDICATORON REMOVES CIRCLE
            tk.Radiobutton(star_frame,text="★",variable=var,value=i,indicatoron=0,width=3,font=('Arial', 14),bg='gold').pack(side='left', padx=2)

    def save_review():
        #GETS VALUE FROM EACH KEY IN DICT-VAR-INTVAR
        story = rating_vars["Story"].get()
        screenplay = rating_vars["Screenplay"].get()
        acting = rating_vars["Acting"].get()
        direction = rating_vars["Direction"].get()
        music = rating_vars["Music"].get()
        visual = rating_vars["Visual Effects"].get()
        entertainment = rating_vars["Entertainment"].get()

        total = story +screenplay +acting +direction +music +visual + entertainment
        avg = total / 7

        #INSERT DATA INTO SQL TABLE
        try:
            con = psq.connect(**db_config)
            cur = con.cursor()
            cur.execute("INSERT INTO reviews(username,movie_name,story,screenplay,acting,direction,music,visual_effects,entertainment,avg_rating)"
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(current_user,movie_name,story,screenplay,acting,direction,music,visual,entertainment,avg))
            con.commit()
            con.close()

            #DISPLAYS SUCCESS MSG BY ROUNDING OFF AVG RATING TO 1 DECIMAL
            messagebox.showinfo("Success",f"Review Saved!\nAverage Rating: {round(avg,1)} ★")
            review_win.destroy()

        except:
            pass

    tk.Button(review_win,text="Submit Review",font=('Arial', 14, 'bold'),bg='red',fg='white',command=save_review).pack(pady=20)

#-------------MOVIE DETAILS SYSTEM-----------------------
def open_details_window(movie):
    #GETTING DATA FROM API 
    title = movie.get("title")
    overview = movie.get("overview" )
    release_date = movie.get("release_date" )
    
    #SIDE WINDOW details_win
    details_win = tk.Toplevel(base)
    details_win.title(f"{title} - Details")
    details_win.geometry("600x400")
    details_win.config(bg='white')
    
    #MOVIE TITLE
    tk.Label(details_win, text=title, font=('Arial', 20, 'bold'), bg='white', wraplength=550).pack(pady=15)
    
    #CREATING INFOFRAME IN DETAILS WIN
    info_frame = tk.Frame(details_win, bg='white')
    info_frame.pack(pady=5)
    # ADDING RELEASE DATE IN THAT
    tk.Label(info_frame, text=f"Release Date: {release_date}", font=('Arial', 12, 'bold'), bg='white').pack(side=tk.LEFT, padx=20)
    
    #MOVIE DESCRIPTION
    tk.Label(details_win, text="Synopsis:", font=('Arial', 14, 'bold'), bg='white').pack(pady=(15, 5))
    tk.Message(details_win, text=overview, font=('Arial', 12), bg='white', width=550, justify=tk.CENTER).pack(pady=5)
    
    #CLOSE BUTTON
    tk.Button(details_win, text="Close", font=('Arial', 12, 'bold'), bg='red', fg='white', command=details_win.destroy).pack(pady=20)

# FETCH MOVIE AND DISPLAY IN GRID
def load_api_movies(search_query=""):
    #DELETES EXISTING MOVIES IN FRAME
    for widget in scrollable_movie_frame.winfo_children():
        widget.destroy()

    if search_query == "": #EMPTY CHECK-DISPLAY WHATEVER THERE
        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    else: #NOT EMPTY-DISPLAY WHAT IS SEARCHED
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={search_query}"

    try:
        response = requests.get(url)
        if response.status_code == 200: #WHEN SITE RUNS AND GIVES OUTPUT-200 DEFAULT STATUS CODE
            data = response.json() #data IS DICT WITH KEY-REQUESTS AND ENTIRE MOVIE LIST-VALUE
            results = data.get("results") #results IS ENTIRE MOVIE LIST
            row = 0
            col = 0
            max_columns = 4 #1 LINE SHOULD CONTAIN ONLY 4 MOVIES

            for movie in results[:10]: #DISPLAY 10 MOVIES
                title = movie.get("title")
                poster_path = movie.get("poster_path") #PATH FROM API DATABASE
                
                movie_card = tk.Frame(scrollable_movie_frame, bg='white', bd=1, relief="solid")
                movie_card.grid(row=row, column=col, padx=15, pady=15)
                
                if poster_path:
                    img_url = f"https://image.tmdb.org/t/p/w200{poster_path}"
                    try:
                        img_response = requests.get(img_url) #URL LINK
                        img_data = img_response.content #ACTUAL IMAGE CONTENT
                        img_data = Image.open(io.BytesIO(img_data)) #USING IO MODULE OPEN IMAGE(FILE HANDLER)
                        img_data = img_data.resize((150, 225)) #RESIZE TO FIT WINDOW
                        photo = ImageTk.PhotoImage(img_data) #FINAL
                        img_label = tk.Label(movie_card, image=photo, bg='white')
                        img_label.image = photo #VARIABLE TO STORE
                        img_label.pack(pady=5, padx=5)
                    except:
                        pass
                else:
                   pass
                #TITLE CONDITION FOR BIG MOVIE NAMES
                if len(title) > 22 :
                    title = title[:19] + "..."

                tk.Label(movie_card, text=title, font=('Arial', 10, 'bold'), bg='white').pack(pady=(0, 5))
                col += 1
                if col >= max_columns:
                    col = 0
                    row += 1
                
                 #SEE DETAILS BUTTON 
                tk.Button(movie_card, text="See Details", bg='blue', fg='white', command=lambda m=movie: open_details_window(m)).pack(pady=2)

                #ADD REVIEW BUTTON
                tk.Button(movie_card,text="Add Review",bg='black',fg='white',command=lambda m=movie: open_review_window(m)).pack(pady=5)
                    
    except :
        pass


    # Force tkinter to calculate the frame's new height, then update the canvas bounds
    scrollable_movie_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

# ---------------- INITIALIZATION ----------------
init_db()
show_login_screen()
base.mainloop()