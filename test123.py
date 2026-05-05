def init_db2():
    con = psq.connect(**db_config)
    cur = con.cursor()
    cur.execute("Create table if not exists admindetails(username varchar(30) primary key,password varchar(20) not null")
    con.commit()
    con.close()

def adminlogin():
    