# from unittest import result
import datetime
import mysql.connector
from datetime import date


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def drview():
       mycursor.execute("SELECT DID, Name, Specialization FROM doctors")
       myresult = mycursor.fetchall()
       data={
              #'message':"data retrieved",
              'rec':myresult,
              #'header':row_headers
              }
       return data

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="surgery"
)

mycursor = mydb.cursor()

def compare_date(appdate):
    today = date.today()
    if today.year<=appdate.year:
        if today.month<=appdate.month:
            if today.day<appdate.day:
                return True
    else:
        return False


num=0
mycursor.execute("SELECT date FROM appointments")
myresult = mycursor.fetchall()
for x in range(len(myresult)):
       if compare_date(myresult[x][0]):
              num+=1
mycursor.execute("SELECT COUNT(DID) FROM doctors")
myresultdoc = mycursor.fetchone()
mycursor.execute("SELECT COUNT(PID) FROM patients")
patmyresult = mycursor.fetchone()
adminlist={'countapp':num,
              'countdoc':myresultdoc[0],                
              'countpat':patmyresult[0]                }
print(adminlist['countapp'])



# print(compare_date(datetime.date(2022, 6, 15)))
no=0
# print(no)
# no+=1
# print(no)
# no+=1
# print(no)
# no+=1
# print(no)

# mycursor.execute("SELECT date FROM appointments")
# myresult = mycursor.fetchall()
# for x in range(len(myresult)):
#        if compare_date(myresult[x][0]):
#               no+=1

# print( no)


# mycursor.execute("SELECT name, Surgery_name, photo_path, phone,email, Birthdate FROM doctors INNER JOIN surgery ON Specialization=idSurgery")
# myresult=mycursor.fetchall()
# doctors=[]
# for x in range(len(myresult)):
#        temp=[]
#        temp.append(myresult[x][0])
#        temp.append(myresult[x][1])
#        if myresult[x][2]:
#               temp.append(myresult[x][2])
#        else :
#               temp.append('static\images\doctor.png')
#        temp.append(myresult[x][3])
#        temp.append(myresult[x][4])
#        temp.append(calculate_age( myresult[x][5]))
#        doctors.append(temp)
# doctors=tuple(doctors)
# print( doctors)

# mycursor.execute("SELECT name, Surgery_name, photo_path FROM doctors INNER JOIN surgery ON Specialization=idSurgery")
# myresult=mycursor.fetchall()
# doctors=[]

# for x in range(len(myresult)):
#        temp=[]
#        temp.append(myresult[x][0])
#        temp.append(myresult[x][1])
#        if myresult[x][2]:
#               temp.append(myresult[x][2])
#        else :
#               temp.append('static\images\doctor.png')
#        doctors.append(temp)

# # patients.append(myresult[0][3])
# # patients.append(myresult[0][4])
# # patients.append(calculate_age(myresult[0][-1]))

# doctors=tuple(doctors)
# print(doctors)


# mycursor.execute("SELECT * FROM patients WHERE email='dodo@hotmail.com'")
# myresult=mycursor.fetchall()
# if myresult:
#   print (myresult[0][-1])
# else:
#   print(None)

# print (myresult)
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
# mycursor.execute("SELECT COUNT(DID) FROM doctors")
# myresult = mycursor.fetchone()
# print(myresult)


