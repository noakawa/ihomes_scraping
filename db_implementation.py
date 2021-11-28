import mysql.connector
import os
import private_info

mydb = mysql.connector.connect(
    host=private_info.HOST,
    user=private_info.USER,
    password=private_info.PASS,
    database="ihomes"
)

mycursor = mydb.cursor()

mycursor.execute()

# data = os.system("python web_scrap.py -c ak")
# print(data)
