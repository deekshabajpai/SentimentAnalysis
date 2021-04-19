from flask import Flask,render_template,request,redirect,session
import mysql.connector
from sentiments import second
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)
app.register_blueprint(second)

try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="users")
    cursor=conn.cursor()
except:
    print("An exception occured")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * from `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/login')


@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute("""INSERT INTO `users` (`name`,`email`,`password`) VALUES ('{}','{}','{}')""".format(name,email, password))
    conn.commit()
    cursor.execute("""SELECT * from `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)