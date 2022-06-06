import datetime
from itertools import count
from re import S
from flask import Flask , render_template,request, session, redirect ,flash,url_for,jsonify
import mysql.connector
from datetime import date
from werkzeug.utils import secure_filename
import os
from flask_mail import Mail, Message


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
#    passwd="",
#    database="surgery"
  passwd="abcd1234",
  database="surgery"
#   passwd="mysql",
#   database="ourdatabase"
)
mycursor = mydb.cursor()

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hospitalteam@hotmail.com'
app.config['MAIL_PASSWORD'] = 'Project1234'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail= Mail(app)


UPLOAD_FOLDER = "static/uploads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
 


#main page route
@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
       if "login" in request.form :
         found=account_search()
         global patient1
         global admn
         if found:
            session['loggedIn']=True 
            email= request.form['email']     
            mycursor.execute("SELECT category FROM users WHERE email=%s",(email,))
            categ=mycursor.fetchone()
            
            if categ==(1,):
               patient1=email
               myresult=patinfo()
               flash("You have logged in succesfully",category="success")
               if myresult[0][-1]:
                photo=myresult[0][-1]
               else:
                   photo='static\images\profile.jpg'
               return render_template('profile.html',datap=myresult, user_image=photo)
            
            elif categ==(2,):
                global dr1 
                dr1=email
                myresult=drinfo()
                if myresult[0][-1]:
                    photo=myresult[0][-1]
                else:
                   photo='static\images\doctor.png'
             #   flash("You have logged in succesfully",category="success")
                return render_template('doctor.html',data=myresult, user_image=photo)
                 
            elif categ==(3,):
            
               admn=email
               myresult=admninfo()
               count=admincount() 
               appoin=appoin_table() 
               doc=adminView()
            #   return render_template("admin.html", docno=docno[0],DATA=myresult,app=appoin,doc=doc)
               return render_template("admin.html", DATA=myresult, count=count,app=appoin,doc=doc)
                
         else:
          mes1="Incorrect password or email,please try again."
          flash(mes1,category="error")
          return render_template('index.html')
          
       elif 'register' in request.form :
        email = request.form['email'].lower()
        password1 = request.form['password']
        password2 = request.form['password_confirmation']
        f_name = request.form['fname'].capitalize()
        l_name = request.form['lname'].upper()
        bd = request.form['bd date']
        phone_no = request.form['phone']
        gender= request.form['switch']
        
        mycursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        found=mycursor.fetchone()
        if found:
            mes = "email already exists."
            flash(mes,category="error") 
            return render_template('index.html')
        elif password1 != password2:
           mes2= "Passwords don't match"
           flash(mes2,category="error") 
           return render_template('index.html')  
        elif len(password1) < 7:
            mes3="Password must be at least 7 characters."
            flash(mes3,category="error") 
            return render_template('index.html')    
        else:
             sql1 = "INSERT INTO users (email,password,category) VALUES (%s, %s, %s)"
             sql2 = "INSERT INTO patients(first_name, Gender, Birthdate, phone ,email ,last_name) VALUES (%s, %s, %s,%s,%s,%s)"
             
             val1 = (email,password1,'1')
             val2 = (f_name, gender, bd, phone_no , email ,l_name)
             
             mycursor.execute(sql1, val1)
             mycursor.execute(sql2, val2)
             mydb.commit() 
             patient1=email
             myresult=patinfo()
             flash("Your account has been created suceesfully",category="success")
             return render_template('profile.html',datap=myresult)
    else:                 
     return render_template('index.html')
    

#patient routes

@app.route('/plogin',methods=['POST','GET'])
def pat_login():
        myresult=patinfo() 
        if myresult[0][-1]:
          photo=myresult[0][-1]
        else:
            photo='static\images\profile.jpg'
        return render_template('profile.html',datap=myresult,user_image=photo)
    
@app.route('/pview',methods=['POST','GET'])
def pat_view():
        myresult=patinfo() 
        drl=adminView()
        return render_template('doctor-patients.html',datap=myresult,dataaa=drl)
        
    
    
@app.route('/appoin',methods=["POST","GET"])
def book():
    email=patient1
    myresult=patinfo()
    if request.method == 'POST':
        surgery = request.form['surgery']
        surgeon = request.form['consultant']
        time= request.form['time']
        date= request.form['date']
        mycursor.execute("SELECT * FROM appointments WHERE  DID =%s AND time =%s  AND date=%s ",(surgeon,time,date,))
        found=mycursor.fetchone()
        if found:
            mes = "This appointment is not available, please choose another time or date"
            flash(mes,category="error") 
            return redirect('/appoin')   
        else:
           mycursor.execute("SELECT PID FROM patients WHERE email=%s",(email,))
           cal=mycursor.fetchone()    
           PID=cal[0]
           sql = "INSERT INTO appointments (surgery, DID,PID,time,date) VALUES (%s, %s,%s, %s,%s)"      
           val = (surgery,surgeon,PID,time,date)
           mycursor.execute(sql, val)
           mydb.commit() 
           mes = "Your appointment is successfully booked"
           flash(mes,category="success") 
           return redirect('/pcal')

    else:   
      mycursor.execute("SELECT * FROM surgery ")
      surgeries = mycursor.fetchall()
      return render_template('appointment.html', surgeries=surgeries,datap=myresult)
  
@app.route('/pcal')
def calender():
    email=patient1
    mycursor.execute("SELECT PID FROM patients WHERE email=%s",(email,))
    cal=mycursor.fetchone()    
    pid=cal[0]
    mycursor.execute("SELECT Surgery_name,date,time FROM appointments INNER JOIN surgery ON surgery= idSurgery WHERE PID=%s",(pid,))
    calendar = mycursor.fetchall()  
    mycursor.execute("SELECT Surgery_name,date,time FROM surgery_schedule INNER JOIN doctors ON surgery_schedule.DID= doctors.DID JOIN surgery on Specialization=idSurgery WHERE PID=%s",(pid,))
    surgeries = mycursor.fetchall()  
    return render_template('calender.html', calendar = calendar,surgeries=surgeries)

@app.route('/contact',methods=["POST","GET"])
def contact():
    email=patient1
    myresult=patinfo()
    if request.method == 'POST':
        message = request.form['mail']
        msg = Message(subject="Hello",body=f"{email}\n{message}" ,sender = 'hospitalteam@hotmail.com', recipients = ['mariammeccawi@hotmail.com'])
        mail.send(msg)
        flash("Message sent successfully!",category="success")
    return render_template('contact.html',datap=myresult)

#admin routes   

@app.route('/alogin')
def admin():
   myresult=admninfo()  
   appoin=appoin_table()
   drdata=drview()
   patdata=patview()
   count= admincount()
   doc=adminView()
 
#    return render_template('admin.html',DATA=myresult,drdata=drdata, patdata=patdata, docno=docno[0],app=appoin,doc=doc) 
   return render_template('admin.html',DATA=myresult,drdata=drdata, patdata=patdata, count=count,app=appoin,doc=doc) 
    
@app.route('/aedit',methods = ['POST', 'GET'])
def editdrs():  
    myresult=admninfo()
    return render_template("edit-doctors.html",DATA=myresult) 
    
    
    
     
    
@app.route('/addd',methods = ['POST', 'GET'])
def adddoctor():
   myresult=admninfo()
   if request.method == 'POST': 
      Name= request.form['Name'].capitalize()
      Password = request.form['Password']
      Gender= request.form['Gender']
      Phone= request.form['Phone']
      Specialization= request.form['Specialization']
      email= request.form['Email'].lower()
      Birthdate= request.form['Birthdate']

      sql1= "INSERT INTO users (email,password,category) VALUES (%s,%s, %s)"
      val1= (email,Password,2)

      sql2= sql2= "INSERT INTO Doctors (Name,gender,phone,Specialization,email,Birthdate) VALUES (%s,%s, %s,%s, %s,%s)"
      val2= (Name,Gender,Phone,Specialization,email,Birthdate)
      
      mycursor.execute(sql1, val1)
      mycursor.execute(sql2, val2)
      mydb.commit() 
      count= admincount()
      doc=adminView()
      return render_template("admin.html",count=count,doc=doc,DATA=myresult)
   else:
       return render_template("hospital-add-doctor.html",DATA=myresult)

@app.route('/addp',methods = ['POST', 'GET'])
def addpatient():
    myresult=admninfo()
    if request.method == 'POST': 
      firstName= request.form['firstname'].capitalize()
      lastName= request.form['lastname'].upper()
      email= request.form['email'].lower()
      Password = request.form['password']
      Gender= request.form['gender']
      Phone= request.form['phone']
      Birthdate= request.form['dateofbirth']

      sql1= "INSERT INTO users (email,password,category) VALUES (%s,%s, %s)"
      val1= (email,Password,1)

      sql2= sql2= "INSERT INTO patients (first_name,last_name,Gender,Phone,email,Birthdate) VALUES (%s,%s, %s,%s, %s,%s)"
      mycursor.execute(sql1, val1)
      val2= (firstName,lastName,Gender,Phone,email,Birthdate)
      mycursor.execute(sql2, val2)
      mydb.commit() 
      count= admincount()
      doc=adminView()
      return render_template("admin.html",count=count,doc=doc,DATA=myresult)
    else:
       return render_template("hospital-add-patient.html",DATA=myresult)
       
@app.route('/listd')
def viewdoctor():
     doct=adminView()
     myresult=admninfo()
     return render_template('hospital-ad-doctors-list.html',DATA=myresult,datarr=doct) 
     
@app.route('/listp')
def viewpatient():
    
    result=admninfo()
    mycursor.execute("SELECT PID, last_name,first_name ,Email,Gender,birthdate FROM patients")
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    patients=[]
    for x in range(len(myresult)):
        temp=[]
        temp.append(myresult[x][0])
        temp.append(myresult[x][2]+" "+myresult[x][1])

        temp.append(myresult[x][3])
        temp.append(myresult[x][4])
        temp.append(calculate_age(myresult[x][5]))
        pat=tuple(temp)
        patients.append(pat)
    data1={
            #'message':"data retrieved",
            'rec':patients,
            'header':row_headers
            } 
    return render_template('hospital-ad-patients-list.html',patdata=data1,DATA=result)
    

#doctor routes
 
@app.route('/dlogin')
def doctor():
     myresult=drinfo()
     return render_template('doctor.html',data=myresult)    
   
@app.route('/u', methods = ['POST', 'GET'])
def user_prof():
    myresult=drinfo()
    if myresult[0][-1]:
        photo=myresult[0][-1]
    else:
        photo='static\images\doctor.png'
    #   flash("You have logged in succesfully",category="success")
    return render_template('users-profile.html',data=myresult, user_image=photo)
 
@app.route('/dappoin',methods=["POST","GET"])
def drappoin():
    email=dr1
    myresult=drinfo()
    if request.method == 'POST':
        pat = request.form['patient']
       # time= request.form['time']
        date= request.form['date']
        mycursor.execute("SELECT COUNT(surg_id) FROM surgery_schedule WHERE date=%s ",(date,))
        x=mycursor.fetchone()
        if (x[0]>2):
            mes = "This day is not available , please choose another date"
            flash(mes,category="error") 
            return redirect('/dappoin')   
        else:
           if (x[0]==0):
            time ="10:00" 
           elif (x[0]==1):
            time ="13:30"
           elif (x[0]==2):
            time="17:00"
           mycursor.execute("SELECT DID FROM doctors WHERE email=%s",(email,))
           cal=mycursor.fetchone()    
           did=cal[0]  
           sql = "INSERT INTO surgery_schedule (DID,PID, time, date) VALUES (%s,%s, %s, %s)"      
           val = (did,pat,time,date)
           mycursor.execute(sql, val)
           mydb.commit() 
           mes = "Surgery is successfully reserved at " +time
           flash(mes,category="success") 
           return redirect('/dappoin')
        #    return render_template('hospital-book-appointment.html',data=myresult) 
        
        # x= mycursor.execute("SELECT * FROM surgery_schedule WHERE  date=%s ",(date,))
        # found=mycursor.fetchone()
        # if found:
        #     # mes = "This appointment is not available, please choose another time or date"
        #     # flash(mes,category="error") 
        #     # return redirect('/appoin')   
        # else:
        #   sql = "INSERT INTO appointments (surgery, DID, time,date) VALUES (%s, %s, %s,%s)"      
        #   val = (surgery,surgeon,time,date)
        #   mycursor.execute(sql, val)
        #   mydb.commit() 
        #   mes = "Your appointment is successfully reserved"
        #   flash(mes,category="success") 
        #   return redirect('/plogin')
    else:
      mycursor.execute("SELECT DISTINCT patients.PID, first_name, last_name FROM appointments INNER JOIN patients ON appointments.PID= patients.PID ")
      patients = mycursor.fetchall()
      return render_template('hospital-book-appointment.html',patients=patients,data=myresult)     

@app.route('/dsched')
def drsched():
     myresult=drinfo()
     mycursor.execute("SELECT Surgery_name,date,time FROM appointments INNER JOIN surgery ON surgery= idSurgery ")
     calendar = mycursor.fetchall()  
     return render_template('hospital-doctor-schedule.html',calendar = calendar,data=myresult)   
   
@app.route('/dlist')
def drlist():
     myresult=drinfo()
     drl=adminView()
     return render_template('hospital-doctors-list.html',data=myresult,dataaa=drl)   

@app.route('/dredit',methods=['POST','GET'])
def dredit():
    myresult= drinfo()
    if request.method == 'POST':
        
        id = myresult[0][0]
        Name =request.form['fullName']
        Gender =request.form['gender']
        Phone =request.form['phone'],
        Phone = Phone[0]
        Specialization =request.form['Specialization']
        Birthdate = request.form['Birthdate']
        print(Name,Gender,Phone,Specialization,Birthdate,id)

        sql1 = "UPDATE doctors SET name=%s,gender=%s,phone=%s,Specialization=%s,Birthdate=%s WHERE DID=%s"
        val1 = (Name,Gender,Phone,Specialization,Birthdate,id) 
        mycursor.execute(sql1, val1)  
        mydb.commit()   

        flash("Data Updated Successfully")
        
        myresult=drinfo()
        if myresult[0][-1]:
            photo=myresult[0][-1]
        else:
            photo='static\images\doctor.png'
        return render_template('doctor.html',data=myresult, user_image=photo)

@app.route('/docpass',methods=['POST','GET'])  
def docpass():
    myresult=drinfo()
    if request.method == 'POST':

        currpass = request.form['password']
        newpass =  request.form['newpassword']
        renewpass= request.form['renewpassword']

        tempemail= myresult[0][5]
        print (tempemail )
        mycursor.execute("SELECT password FROM users WHERE email=%s",(tempemail,))
        oldpass = mycursor.fetchone()
        oldpass = oldpass [0]
        print (oldpass )
        if oldpass==currpass:
            if newpass==renewpass:
                
                print (newpass,tempemail)
                sql2 = "UPDATE users SET password=%s  WHERE email=%s "
                val2 = (renewpass,tempemail) 
                mycursor.execute(sql2, val2)
                mydb.commit() 
                myresult=drinfo()
                return render_template('index.html')

            else :   
              flash("New Password Mismatch ")
              myresult=drinfo()
              if myresult[0][-1]:
                photo=myresult[0][-1]
              else:
                photo='static\images\doctor.png'
             #   flash("You have logged in succesfully",category="success")
            return render_template('doctor.html',data=myresult, user_image=photo)
          
        else :
              flash("current password is wrong ")
              if myresult[0][-1]:
                photo=myresult[0][-1]
              else:
                photo='static\images\doctor.png'
             #   flash("You have logged in succesfully",category="success")
        return render_template('doctor.html',data=myresult, user_image=photo)
   
   
#functions

def account_search():
    email= request.form['email']
    password= request.form['password']
    mycursor.execute("SELECT * FROM users WHERE email=%s AND password=%s",(email,password,))
    found=mycursor.fetchone()
    return found

@app.route('/consultant/<category_id>/',methods=["POST","GET"])
def consultant(category_id):  
    mycursor.execute("SELECT * FROM doctors WHERE specialization = %s ", (category_id,))
    consultants = mycursor.fetchall()  
    OutputArray = []
    for row in consultants:
        outputObj = {
            'id': row[0],
            'name': row[1]}
        OutputArray.append(outputObj)
    return jsonify({'consultants':OutputArray})

@app.route('/time/<category_id2>/',methods=["POST","GET"])
def time(category_id2):  
    
    mycursor.execute("SELECT working_times FROM doc_schedule WHERE DID = %s ", (category_id2,))
    times = mycursor.fetchall()  
    OutputArray = []
    for row in times:
        outputObj = {
            'time': row}
        OutputArray.append(outputObj)
    return jsonify({'times':OutputArray})

@app.route('/pedit',methods=['POST','GET'])
def pedit():
    myresult=patinfo()
    if request.method == 'POST':
        id = myresult[0][0]
        fname = request.form['firstName']
        lname = request.form['lastName']
        Phone = request.form['phone']
        # Email= request.form['email']
        Birthdate = request.form['bdate']
        Gender= request.form['gender']
        sql2 = "UPDATE patients SET First_name=%s,Gender=%s,Birthdate=%s,Phone=%s,Last_Name=%s WHERE PID=%s"
        val2 = (fname,Gender,Birthdate,Phone,lname,id) 
        mycursor.execute(sql2, val2)     
        flash("Data Updated Successfully")
        mydb.commit() 
        myresult=patinfo()
        if myresult[0][-1]:
                  photo=myresult[0][-1]
        else:
                   photo='static\images\profile.jpg'
        return render_template('profile.html',datap=myresult, user_image=photo)
        
   
@app.route('/patpass',methods=['POST','GET'])  
def patpass():
    myresult=patinfo()
    if request.method == 'POST':
        currpass = request.form['password']
        newpass =  request.form['newpassword']
        renewpass= request.form['renewpassword']

        tempemail= myresult[0][5]
        print (tempemail )
        mycursor.execute("SELECT password FROM users WHERE email=%s",(tempemail,))
        oldpass = mycursor.fetchone()
        oldpass = oldpass [0]
        print (oldpass )
        if oldpass==currpass:
            if newpass==renewpass:
                
                print (newpass,tempemail)
                sql2 = "UPDATE users SET password=%s  WHERE email=%s "
                val2 = (renewpass,tempemail) 
                mycursor.execute(sql2, val2)
                # mycursor.execute (f"UPDATE users SET password={newpass}  WHERE email={tempemail} ")  
                mydb.commit() 
                myresult=patinfo()
                if myresult[0][-1]:
                        photo=myresult[0][-1]
                else:
                        photo='static\images\profile.jpg'
                return render_template('index.html',datap=myresult, user_image=photo)

            else :   
              flash("New Password Mismatch ")
              myresult=patinfo()
              if myresult[0][-1]:
                        photo=myresult[0][-1]
              else:
                        photo='static\images\profile.jpg'
              return render_template('profile.html',datap=myresult ,user_image=photo)
          
        else :
                flash("current password is wrong ")
                if myresult[0][-1]:
                        photo=myresult[0][-1]
                else:
                        photo='static\images\profile.jpg'
        return render_template('profile.html',datap=myresult, user_image=photo)

@app.route('/patphoto',methods=['POST','GET'])  
def patphoto():
    myresult=patinfo()
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        myresult=patinfo()
        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        NOW = datetime.datetime.now()
        new_filename = os.path.join(UPLOAD_FOLDER, file.filename.rsplit('.',1)[0] + '_' + NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + file.filename.rsplit('.',1)[1])
        file.save(new_filename)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        path=new_filename
        tempemail= myresult[0][5]
        # cursor.execute("INSERT INTO fruit (name, variety) VALUES (%s, %s)", (new_fruit, new_fruit_type));
        mycursor.execute("UPDATE patients SET photo_path= %s WHERE email= %s ;",(path,tempemail));
        mydb.commit()
        myresult=patinfo()
        if myresult[0][-1]:
            photo=myresult[0][-1]
        else:
                   photo='static\images\profile.jpg'
               
        return render_template('profile.html', filename=filename,datap=myresult, user_image=photo)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/drphoto',methods=['POST','GET'])  
def drphoto():
    myresult=drinfo()
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        myresult=drinfo()
        filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        NOW = datetime.datetime.now()
        new_filename = os.path.join(UPLOAD_FOLDER, file.filename.rsplit('.',1)[0] + '_' + NOW.strftime("%d_%m_%Y_%H_%M_%S") + '.' + file.filename.rsplit('.',1)[1])
        file.save(new_filename)
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        path=new_filename
        tempemail= myresult[0][5]
        # cursor.execute("INSERT INTO fruit (name, variety) VALUES (%s, %s)", (new_fruit, new_fruit_type));
        mycursor.execute("UPDATE doctors SET photo_path= %s WHERE email= %s ;",(path,tempemail));
        mydb.commit()
        myresult=drinfo()
        if myresult[0][-1]:
            photo=myresult[0][-1]
        else:
                   photo='static\images\doctor.png'
               
        return render_template('users-profile.html', filename=filename, data=myresult, user_image=photo)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/patdelete/<int:record_id>', methods = ['POST', 'GET'])
def patdelete(record_id):
      flash("Record Has Been Deleted Successfully")
      mycursor.execute(f"SELECT email FROM patients WHERE PID = {record_id}")
      email = mycursor.fetchone()
      sql1= "DELETE FROM users WHERE email = %s"
      sql2 = f"DELETE FROM patients WHERE PID = {record_id}"
      mycursor.execute(sql2)
      mycursor.execute(sql1, email) 
      mydb.commit()  
      return   redirect(url_for('admin'))

@app.route('/drdelete/<int:record_id>', methods = ['POST', 'GET'])
def drdelete(record_id):
      flash("Record Has Been Deleted Successfully")
      mycursor.execute(f"SELECT email FROM doctors WHERE DID = {record_id}")
      email = mycursor.fetchone()
      sql1= "DELETE FROM users WHERE email = %s"
      sql2 = f"DELETE FROM doctors WHERE DID = {record_id}"
      mycursor.execute(sql2)
      mycursor.execute(sql1, email) 
      mydb.commit()  
      return   redirect(url_for('admin'))
  
def drview():
       mycursor.execute("SELECT DID, Name, Specialization FROM doctors")
       myresult = mycursor.fetchall()
       data={
              #'message':"data retrieved",
              'rec':myresult,
              #'header':row_headers
              }
       return data

def patview():
       mycursor.execute("SELECT PID, first_name,email FROM patients")
       myresult = mycursor.fetchall()
       data={
              #'message':"data retrieved",
              'rec':myresult,
              #'header':row_headers
              }
       return data

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def compare_date(appdate):
    today = date.today()
    if today.year<=appdate.year:
        if today.month<=appdate.month:
            if today.day<appdate.day:
                return True
    else:
        return False

# def countapp():
#         no=0
#         mycursor.execute("SELECT date FROM appointments")
#         myresult = mycursor.fetchall()
#         for x in range(len(myresult)):
#             if compare_date(myresult[x][0]):
#               no+=1
#         return no

def admincount():
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
    mycursor.execute("SELECT COUNT(appointment_id) FROM appointments")
    appmyresult = mycursor.fetchone()
    adminlist={'countapp':num,
                'countdoc':myresultdoc[0],                
                'countpat':patmyresult[0],  
                'counttapp':appmyresult[0]              }
    return adminlist
     
# def countdoc():
#      mycursor.execute("SELECT COUNT(DID) FROM doctors")
#      myresult = mycursor.fetchone()
#      return myresult

# def countpat():
#      mycursor.execute("SELECT COUNT(PID) FROM patients")
#      myresult = mycursor.fetchone()
#      return myresult

def patinfo():
    email=patient1
    mycursor.execute("SELECT * FROM patients WHERE email=%s",(email,))
    myresult=mycursor.fetchall()     
    return myresult;
               
def drinfo():
    email=dr1
    mycursor.execute("SELECT * FROM doctors WHERE email=%s",(email,))
    myresult=mycursor.fetchall()     
    return myresult;         

def admninfo():
    email=admn
    mycursor.execute("SELECT * FROM admins WHERE email=%s",(email,))
    myresult=mycursor.fetchall()     
    return myresult;   
    
def appoin_table():
     mycursor.execute("SELECT * FROM appointments JOIN surgery ON surgery=idSurgery")
     myresult=mycursor.fetchall()   
     return myresult  
 
# def surgery_table():
#     mycursor.execute("SELECT * FROM patients")
#     myresult=mycursor.fetchall()
#     return myresult  
  
def get_doctors():
    mycursor.execute("SELECT* FROM doctors INNER JOIN surgery ON Specialization=idSurgery")
    myresult=mycursor.fetchall()
    return myresult

def adminView():
    mycursor.execute("SELECT name, Surgery_name, photo_path, phone,email, Birthdate,DID FROM doctors INNER JOIN surgery ON Specialization=idSurgery")
    myresult=mycursor.fetchall()
    doctors=[]
    for x in range(len(myresult)):
        temp=[]
        temp.append(myresult[x][0])
        temp.append(myresult[x][1])
        if myresult[x][2]:
                temp.append(myresult[x][2])
        else :
                temp.append('static\images\doctor.png')
        temp.append(myresult[x][3])
        temp.append(myresult[x][4])
        temp.append(calculate_age( myresult[x][5]))
        temp.append( myresult[x][6])
        doctors.append(temp)
    doctors=tuple(doctors)
    return doctors
     

  
app.secret_key="super secret key" 
 
 
 
if __name__ == '__main__':
    app.run(debug=True) 
     
    