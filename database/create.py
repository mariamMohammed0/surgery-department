import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="abcd1234", #default = root
  )

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE surgery")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
   print(x)