from re import S
from flask import Flask , render_template,request, session, redirect ,flash,url_for,jsonify
import mysql.connector
from datetime import date


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
#   passwd="mimi2001",
#   database="dbp"
  passwd="abcd1234",
  database="surgdb"
#   passwd="mysql",
#   database="ourdatabase"
)
mycursor = mydb.cursor()
  

app=Flask(__name__)
 
#main page route
@app.route('/',methods=['POST','GET'])
def home(): 
    # docno= countdoc()
    # return(render_template("admin.html",docno=docno[0]))
    if request.method == 'POST':
       if "login" in request.form :
         found=account_search()
         global patient
       
         global admn
         if found:
            session['loggedIn']=True 
            email= request.form['email']     
            mycursor.execute("SELECT category FROM users WHERE email=%s",(email,))
            categ=mycursor.fetchone()
            
            if categ==(1,):
               patient=email
               myresult=patinfo()
               flash("You have logged in succesfully",category="success")
               return render_template('profile.html',datap=myresult)
            
            elif categ==(2,):
                global dr1 
                dr1=email
                myresult=drinfo()
             #   flash("You have logged in succesfully",category="success")
                return render_template('doctor.html',data=myresult)
                 
            elif categ==(3,):
            
              admn=email
              myresult=admninfo()
              docno= countdoc()  
              appoin=appoin_table() 
            #  flash("You have logged in succesfully",category="success")
              return render_template("admin.html", docno=docno[0],DATA=myresult,app=appoin)
                
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
             patient=email
             myresult=patinfo()
             flash("Your account has been created suceesfully",category="success")
             return render_template('profile.html',datap=myresult)
    else:                 
     return render_template('index.html')
    

#patient routes

@app.route('/plogin',methods=['POST','GET'])
def pat_login():
        myresult=patinfo() 
        return render_template('profile.html',datap=myresult)
    
    
@app.route('/appoin',methods=["POST","GET"])
def book():
    email=patient
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
    email=patient
    mycursor.execute("SELECT PID FROM patients WHERE email=%s",(email,))
    cal=mycursor.fetchone()    
    pid=cal[0]
    mycursor.execute("SELECT Surgery_name,date,time FROM appointments INNER JOIN surgery ON surgery= idSurgery WHERE PID=%s",(pid,))
    calendar = mycursor.fetchall()  
    return render_template('calender.html', calendar = calendar)

#admin routes   

@app.route('/alogin')
def admin():
   myresult=admninfo()
   appoin=appoin_table()
  # alldr=get_doctors()
   drdata=drview()
   patdata=patview()
   docno= countdoc()
   return render_template('admin.html',DATA=myresult,drdata=drdata, patdata=patdata, docno=docno[0],app=appoin) 
 
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
      docno= countdoc()
      return render_template("admin.html",docno=docno[0],DATA=myresult)
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
      docno= countdoc()
      return render_template("admin.html",docno=docno[0],DATA=myresult)
    else:
       return render_template("hospital-add-doctor.html",DATA=myresult)

@app.route('/listd')
def viewdoctor():
     doct=get_doctors()
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
    return render_template('users-profile.html',data=myresult)
    
@app.route('/dappoin')
def drappoin():
    myresult=drinfo()
    return render_template('hospital-book-appointment.html',data=myresult)   
   
@app.route('/dsched')
def drsched():
     myresult=drinfo()
     mycursor.execute("SELECT Surgery_name,date,time FROM appointments INNER JOIN surgery ON surgery= idSurgery ")
     calendar = mycursor.fetchall()  
     return render_template('hospital-doctor-schedule.html',calendar = calendar,data=myresult)   
   
@app.route('/dlist')
def drlist():
     myresult=drinfo()
     drl=get_doctors()
     return render_template('hospital-doctors-list.html',data=myresult,dataaa=drl)   
   
   
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
        # return redirect ('/') 
        return render_template('profile.html',datap=myresult)
   
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
                mycursor.execute ("UPDATE users SET password=%S WHERE email=%s ;", (newpass,tempemail))  
                myresult=patinfo()
                return render_template('profile.html',datap=myresult)

            else :   
              flash("New Password Mismatch ")
              myresult=patinfo()
              return render_template('profile.html',datap=myresult)
          
        else :
          flash("current password is wrong ")
          myresult=patinfo()
          return render_template('profile.html',datap=myresult)

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

def countdoc():
     mycursor.execute("SELECT COUNT(DID) FROM doctors")
     myresult = mycursor.fetchone()
     return myresult

def patinfo():
    email=patient
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
  
def get_doctors():
    mycursor.execute("SELECT * FROM surgery JOIN doctors ON Specialization=idSurgery")
    myresult=mycursor.fetchall()
    return myresult
     
    
app.secret_key="super secret key" 
 
 
 
if __name__ == '__main__':
    app.run(debug=True) 
     
    