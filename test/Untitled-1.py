import mysql.connector as psq
import os
from dotenv import load_dotenv
load_dotenv()
con=psq.connect(host=os.getenv("DB_host"),user=os.getenv("DB_user"),password=os.getenv("DB_PASS"),database=os.getenv("DB_Name"))
cur=con.cursor()
cur.execute("desc student;")
for x in cur:
    print(x)
