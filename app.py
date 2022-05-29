from unicodedata import category
from flask import Flask , render_template,request, session, redirect ,flash
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="abcd1234",
  database="surgdb"
)
mycursor = mydb.cursor()

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def home():
    #mes1="" 
    #mes2="" 
    if request.method == 'POST':
       if "login" in request.form :
         found=account_search()
         if found:
            session['loggedIn']=True 
            flash("logged in succesfully",category="success")
            return render_template('index1.html')
           
         else:
          mes1="Incorrect password or email,please try again."
          flash(mes1,category="error")
          
    
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
        elif password1 != password2:
           mes2= "Passwords don't match"
           flash(mes2,category="error")   
        elif len(password1) < 7:
            mes3="Password must be at least 7 characters."
            flash(mes3,category="error") 
            
        else:
             sql1 = "INSERT INTO users (email,password,category) VALUES (%s, %s, %s)"
             sql2 = "INSERT INTO patients (first_name, Gender, Birthdate, phone ,email ,last_name) VALUES (%s, %s, %s,%s,%s,%s)"
             
             val1 = (email,password1,'1')
             val2 = (f_name, gender, bd, phone_no , email ,l_name)
             
             mycursor.execute(sql1, val1)
             mycursor.execute(sql2, val2)
             mydb.commit() 
             return render_template('index1.html')
                     
    return render_template('index.html')

def login():
     return render_template('index1.html')
                            
@app.route('/book')
def book():
       return render_template('book.html')
    
 
 
def account_search():
    email= request.form['email']
    password= request.form['password']
    mycursor.execute("SELECT * FROM users WHERE email=%s AND password=%s",(email,password,))
    found=mycursor.fetchone()
    return found
 
app.secret_key="super secret key" 
 
 
 
if __name__ == '__main__':
    app.run() 
     
    