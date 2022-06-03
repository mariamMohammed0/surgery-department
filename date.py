import mysql.connector
from datetime import date


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mimi2001",
  database="ourdatabase"
)

mycursor = mydb.cursor()


# mycursor.execute("SELECT PID, last_name, last_name,Email,Gender,birthdate FROM patients")
# myresult=mycursor.fetchall()
# patients=[]
# patients.append(myresult[0][0])
# patients.append(myresult[0][1]+", "+myresult[0][2])
# # patients.append(myresult[0][2])
# patients.append(myresult[0][3])
# patients.append(myresult[0][4])
# patients.append(calculate_age(myresult[0][-1]))

# patients=tuple(patients)
# pat=[]
# pat.append(patients)
# # patients=calculate_age(myresult[0][-1])
# # patients[0][1]=myresult[0][1]
# # patients[0][2]=myresult[0][2]
# # patients[0][3]=myresult[0][3] 
# # patients[0][4]=myresult[0][4]
# print(patients)
# data={
#         #'message':"data retrieved",
#         'rec':pat,
#         # 'header':row_headers
#         } 
# for r in data['rec']: 
#     print('############################################')
#     print(r)
#     for l in r:
#         print(l)
mycursor.execute("SELECT COUNT(DID) FROM doctors")
myresult = mycursor.fetchone()
print(myresult)


