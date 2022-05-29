import mysql.connector
from sqlalchemy import VARCHAR


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="abcd1234", # passwd default= root
    database="surgdb"
  )

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE ADMINS (AID int NOT NULL AUTO_INCREMENT , AFname VARCHAR(255) DEFAULT NULL , ALname VARCHAR(255) DEFAULT NULL , Gender VARCHAR(6) DEFAULT NULL , Birthdate date DEFAULT NULL , Phone int DEFAULT NULL , Email VARCHAR(255) DEFAULT NULL , Ausername VARCHAR(255) DEFAULT NULL , PRIMARY KEY(AID)")

#mycursor.execute("CREATE TABLE DOCTORS (DID int NOT NULL AUTO_INCREMENT ,DFname VARCHAR(255) DEFAULT NULL , DLname VARCHAR(255) DEFAULT NULL , Gender VARCHAR(6) DEFAULT NULL , Birthdate date DEFAULT NULL , Phone int DEFAULT NULL, Email VARCHAR(255) DEFAULT NULL, Dusername VARCHAR(255) DEFAULT NULL), Specialization VARCHAR(255) DEFAULT NULL, Degree VARCHAR(255) DEFAULT NULL, PRIMARY KEY(DID)")

#mycursor.execute("CREATE TABLE PATIENTS (PID int NOT NULL  AUTO_INCREMENT ,PFname VARCHAR(255) DEFAULT NULL , PLname VARCHAR(255) DEFAULT NULL , Gender VARCHAR(6) DEFAULT NULL, Birthdate date DEFAULT NULL, Phone int DEFAULT NULL, Email VARCHAR(255) DEFAULT NULL,`Pusername` VARCHAR(255) DEFAULT NULL,`APP_Code` VARCHAR(255) DEFAULT NULL,`Surgery_Code` VARCHAR(255) DEFAULT NULL,PRIMARY KEY(PID)")

#mycursor.execute("CREATE TABLE REPORT (DoctorName VARCHAR(200), PatientName VARCHAR(200), Date DATE NOT NULL, Diagnosis VARCHAR(300), Procedures VARCHAR(300), img VARCHAR(300), mimetype VARCHAR(300))")
  
#mycursor.execute("CREATE TABLE APPOINTMENT (PFname VARCHAR(100), PLname VARCHAR(100), Date&Time DATETIME NOT NULL, mobilephone VARCHAR(12), Department VARCHAR(100))")


  # *********************************** ADD TO DOCTOR *******************************************
sql="INSERT INTO DOCTORS (doctorFname , doctorLname , DID , doctorpassword ,clinicname ,age , gender , mobilephone , salary ,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
value = [
 ('Dina','Salama','D1','1234', 'Dina','21','female','011266672701','99999999','dinakhalid404@gmail.com'),
 ('Fady', 'Nour', 'D2', '1324', 'Fady', '33', 'male', '010555672701', '100000', 'fady20@gmail.com'),
]
mycursor.executemany(sql,value)
mydb.commit()
  
  # *********************************** ADD TO PATIENT *******************************************

sql = "INSERT INTO PATIENTS (patientFname , patientLname , PID , patientpassword , age , gender , mobilephone,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
value = [
('Ereny', 'Eleya', '1', '9876', '21', 'female', '012888888888', 'ereny2022@gmail.com'),
('Ahmed', 'Mohammed', '2', '1368', '25', 'male', '012123456789', 'amohammed@gmail.com'),
('Maryam', 'Ahmed', '3', '1111', '30', 'female', '010888834888', 'maro2020@gmail.com'),
('Nour', 'Emad', '4', '1212', '23', 'female', '011888888222', 'nonoemad@gmail.com'),
]
mycursor.executemany(sql,value)
mydb.commit()

  # *********************************** ADD TO ADMIN *******************************************
sql = "INSERT INTO ADMINS (adminFname , adminLname , AID , adminpassword , age , gender , mobilephone , salary ,  Email ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
value = [
    ('Maha', 'Mohammed', 'A1', '3333', '22', 'female', '012111111111', '5000', 'dmaha@gmail.com'),
    ('Mohamed', 'Gamal', 'A2', '9999', '29', 'male', '010555777777', '7000', 'mgamal@gmail.com'),

  ]

mycursor.executemany(sql,value)
mydb.commit()
