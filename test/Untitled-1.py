"""print("hello world")
print('hi')
print("charan is a loser")
for i in range(2):
    print("we are acing this project!!!!")"""
import mysql.connector as psq
con=psq.connect(host='localhost',user='root',password='2101',database='sandhya')
cur=con.cursor()
cur.execute("select * from student where rollno=101;")
l=cur.fetchall()
print(l)
cur.commit()
