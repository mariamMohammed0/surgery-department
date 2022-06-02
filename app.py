from unicodedata import category
from flask import Flask , render_template,request, session, redirect ,flash,url_for,jsonify
import mysql.connector
from regex import P
from sympy import public

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="abcd1234",
  database="surgery"
)
mycursor = mydb.cursor()
  

app=Flask(__name__)
 
#main page route
@app.route('/',methods=['POST','GET'])
def home(): 
    if request.method == 'POST':
       if "login" in request.form :
         found=account_search()
         if found:
            #categ = get_info()
            session['loggedIn']=True 
            email= request.form['email']     
            mycursor.execute("SELECT category FROM users WHERE email=%s",(email,))
            categ=mycursor.fetchone()
            if categ==(1,):
               mycursor.execute("SELECT * FROM patients WHERE email=%s",(email,))
               myresult=mycursor.fetchall()
               return render_template('profile.html',data=myresult)
            
            elif categ==(2,):
                     return render_template('doctor.html')
                 
            elif categ==(3,):
             #flash("You have logged in succesfully",category="success")
              mycursor.execute("SELECT *  FROM users WHERE email=%s",(email,))
              myresult = mycursor.fetchall()
            #  drdata=drview()
             # patdata=patview()
             # return render_template('users-profile.html', drdata=drdata, patdata=patdata,data=myresult)  
              return render_template('admin.html')
                
           
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
             sql2 = "INSERT INTO patients (first_name, Gender, Birthdate, phone ,email ,last_name) VALUES (%s, %s, %s,%s,%s,%s)"
             
             val1 = (email,password1,'1')
             val2 = (f_name, gender, bd, phone_no , email ,l_name)
             
             mycursor.execute(sql1, val1)
             mycursor.execute(sql2, val2)
             mydb.commit() 
             flash("Your account has been created suceesfully",category="success")
             return render_template('profile.html')
    else:                 
     return render_template('index.html')

#patient routes

@app.route('/plogin',methods=['POST','GET'])
def pat_login():
       # myresult=patinfo()
        return render_template('profile.html')
    
@app.route('/appoin',methods=["POST","GET"])
def book():
    if request.method == 'POST':
        surgery = request.form['surgery']
        surgeon = request.form['consultant']
        time= request.form['time']
        date= request.form['date']

        print(surgery,surgeon,time)
        sql = "INSERT INTO appointments (surgery, DID, time,date) VALUES (%s, %s, %s,%s)"      
        val = (surgery,surgeon,time,date)
        mycursor.execute(sql, val)
        mydb.commit() 
        return redirect('/plogin')
    else:   
      mycursor.execute("SELECT * FROM surgery ")
      surgeries = mycursor.fetchall()
      return render_template('appointment.html', surgeries=surgeries)
 
@app.route('/pcal')
def calender():
       return render_template('calender.html') 
   
   
#admin routes   

@app.route('/alogin')
def admin():
       drdata=drview()
       patdata=patview()
       return render_template('admin.html',drdata=drdata, patdata=patdata)  

@app.route('/u', methods = ['POST', 'GET'])
def adm_prof():
     return render_template('users-profile.html')
 
@app.route('/addd')
def adddoctor():
     return render_template('hospital-add-doctor.html') 
 
@app.route('/addp')
def addpatient():
     return render_template('hospital-add-patient.html')  

@app.route('/listd')
def viewdoctor():
     return render_template('hospital-ad-doctors-list.html') 

@app.route('/listp')
def viewpatient():
     return render_template('hospital-ad-patients-list.html') 
 
 
#doctor routes
 
@app.route('/dlogin')
def doctor():
       return render_template('doctor.html')    
   
@app.route('/dappoin')
def drappoin():
       return render_template('hospital-book-appointment.html')    
   
@app.route('/dsched')
def drsched():
       return render_template('hospital-doctor-schedule.html')   
   
@app.route('/dlist')
def drlist():
       return render_template('hospital-doctors-list.html')   
   
@app.route('/dprof')
def dr_prof():
       return render_template('hospital-doctor-profile.html')          

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


               
    



# def __init__(self, patient=0):   
#     self.patient = patient 
#      #using the getter method   
# # def id(self):   
# #         return self.patient
#       # using the setter method   
# def id(self, a):   
#     self.patient = a   

 
app.secret_key="super secret key" 
 
 
 
if __name__ == '__main__':
    app.run(debug=True) 
     
    