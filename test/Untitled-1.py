import mysql.connector as psq
import mysql.connector as psq
con=psq.connect(host='localhost',user='root',password='2101',database='sandhya')
cur=con.cursor()
def loginpg():
    cur.execute("create table if not exist login(name char(30) not null,age int,gender char(1),email varchar(50),username varchar(30) primary key,password varchar(20) not null,bio varchar(20);")
    con.commit()
    con.close()

