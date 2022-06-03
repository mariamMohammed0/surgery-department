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
         global patient, dr , admn
         if found:
            session['loggedIn']=True 
            email= request.form['email']     
            mycursor.execute("SELECT category FROM users WHERE email=%s",(email,))
            categ=mycursor.fetchone()
            
            if categ==(1,):
               patient=email
               myresult=patinfo()
               return render_template('profile.html',datap=myresult)
            
            elif categ==(2,):
                dr=email
                myresult=drinfo()
                return render_template('doctor.html',data=myresult)
                 
            elif categ==(3,):
             #flash("You have logged in succesfully",category="success")
              admn=email
              myresult=admninfo()
              docno= countdoc()  
              appoin=appoin_table()
              return render_template("admin.html", docno=docno[0],DATA=myresult,app=appoin)
                
         else:
          mes1="Incorrect password or email,please try again."
          flash(mes1,category="error")
          return render_template('index.html')
          
       elif 'register' in request.form :
        email = request.form['email']
        password1 = request.form['password']
        password2 = request.form['password_confirmation']
        f_name = request.form['fname']
        l_name = request.form['lname']
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
    # if request.method == 'POST':
    #    if'edit' in request.form :
    #     fname = request.form['firstName']
    #     lname = request.form['lastName']
    #     phone_no = request.form['phone']
    #     email = request.form['email']
    #     bd = request.form['bdate']
    #     gender= request.form['gender']
        
    #     sql1="UPDATE patients SET first_name=%s,Gender=%s,Birthdate=%s,Phone=%s,email=%s,last_name=%s WHERE email=%s"
    #     val1= (fname,gender,bd,phone_no,email,lname,patient)  
    #     mycursor.execute(sql1, val1)
    #     mydb.commit()  
    #     patient=email
    #     myresult=patinfo() 
    #     return render_template('profile.html')
    # else:  
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
        date= request.form.get('date')
        mycursor.execute("SELECT PID FROM patients WHERE email=%s",(email,))
        cal=mycursor.fetchone()    
        PID=cal[0]
        sql = "INSERT INTO appointments (surgery, DID,PID,time,date) VALUES (%s, %s,%s, %s,%s)"      
        val = (surgery,surgeon,PID,time,date)
        mycursor.execute(sql, val)
        mydb.commit() 
        return render_template('profile.html',datap=myresult)
    else:   
      mycursor.execute("SELECT * FROM surgery ")
      surgeries = mycursor.fetchall()
      return render_template('appointment.html', surgeries=surgeries,datap=myresult)
 
@app.route('/pcal')
def calender():
       return render_template('calender.html') 
   
   
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
      Name= request.form['Name']
      Password = request.form['Password']
      Gender= request.form['Gender']
      Phone= request.form['Phone']
      Specialization= request.form['Specialization']
      email= request.form['Email']
      Birthdate= request.form['Birthdate']

      sql1= "INSERT INTO users (email,password,category) VALUES (%s,%s, %s)"
      val1= (email,Password,2)

      sql2= sql2= "INSERT INTO Doctors (Name,gender,phone,Specialization,email,Birthdate) VALUES (%s,%s, %s,%s, %s,%s)"
      mycursor.execute(sql1, val1)
      val2= (Name,Gender,Phone,Specialization,email,Birthdate)
      mycursor.execute(sql2, val2)
      mydb.commit() 
      docno= countdoc()
      return render_template("admin.html",docno=docno[0],DATA=myresult)
   else:
      return render_template("hospital-add-doctor.html",DATA=myresult)
    #   Name= request.form['Name']
    #   Password = request.form['Password']
    #   Gender= request.form['Gender']
    #   Phone= request.form['Phone']
    #   Specialization= request.form['Specialization']
    #   email= request.form['email']
    #   Birthdate= request.form['Birthdate']

    #   sql1= "INSERT INTO users (email,password,category) VALUES (%s,%s, %s)"
    #   val1= (email,Password,2)
    #   mycursor.execute(sql1, val1)

    #   sql2= "INSERT INTO doctors (Name,gender,phone,Specialization,email,Birthdate) VALUES (%s,%s, %s,%s, %s,%s, %s,%s, %s)"
    #   val2= (Name,Gender,Phone,Specialization,email,Birthdate)
    #   mycursor.execute(sql2, val2)
    #   mydb.commit() 
             
 
@app.route('/addp')
def addpatient():
    myresult=admninfo()
    return render_template('hospital-add-patient.html',DATA=myresult)  

@app.route('/listd')
def viewdoctor():
     myresult=admninfo()
     return render_template('hospital-ad-doctors-list.html',DATA=myresult) 

@app.route('/listp')
def viewpatient():
    result=admninfo()
    mycursor.execute("SELECT PID, last_name,first_name ,Email,Gender,birthdate FROM patients")
    row_headers=[x[0] for x in mycursor.description] #this will extract row headers
    myresult = mycursor.fetchall()
    patients=[]
    patients.append(myresult[0][0])
    patients.append(myresult[0][1]+", "+myresult[0][2])
    # patients.append(myresult[0][2])
    patients.append(myresult[0][3])
    patients.append(myresult[0][4])
    patients.append(calculate_age(myresult[0][-1]))

    patients=tuple(patients)
    pat=[]
    pat.append(patients)
    data1={
            #'message':"data retrieved",
            'rec':pat,
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
     return render_template('hospital-doctor-schedule.html',data=myresult)   
   
@app.route('/dlist')
def drlist():
     myresult=drinfo()
     return render_template('hospital-doctors-list.html',data=myresult)   
   
   
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
    email=dr
    mycursor.execute("SELECT * FROM doctors WHERE email=%s",(email,))
    myresult=mycursor.fetchall()     
    return myresult;         

def admninfo():
    email=admn
    mycursor.execute("SELECT * FROM admins WHERE email=%s",(email,))
    myresult=mycursor.fetchall()     
    return myresult;   
    
  
def appoin_table():
     mycursor.execute("SELECT * FROM appointments")
     myresult=mycursor.fetchall()   
     return myresult  
  
def get_doctors():
    mycursor.execute("SELECT * FROM doctors")
    myresult=mycursor.fetchall()   
    return myresult  
  
    
app.secret_key="super secret key" 
 
 
 
if __name__ == '__main__':
    app.run(debug=True) 
     
    