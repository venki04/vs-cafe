from flask import Flask,render_template, request, redirect, url_for, session , app ,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_login import login_user
import mysql.connector

app = Flask(__name__)
app.debug= True
app.config.update({'TEMPLATES_AUTO_RELOAD': True})

app.secret_key = 'your secret key'

mydb= mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "foodorder"
)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'foodorder'



mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('lgin.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL,% s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('regs.html', msg = msg)

@app.route('/Registered', methods=['POST','GET'])

def Ordered():

    if request.method == 'GET':

        mycursor=mydb.cursor()
        mycursor.execute('SELECT * FROM register WHERE did = %s',(session['id'],))
        data = mycursor.fetchall()
        mycursor.close()
        return render_template('Ordered.html',register=data)

@app.route('/about',methods=['GET','POST'])
def about():
    msg=''
    if request.method == 'POST':
        fname = request.form['fname']
        lname= request.form['lname']
        country = request.form['country']
        subject = request.form['subject']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO contactus VALUES (NULL,% s, % s, % s, % s)", (fname,lname,country,subject,))
        mysql.connection.commit()
        msg = 'Sent Successfully'
    return render_template('about.html',msg=msg)



@app.route('/reserve', methods =['GET', 'POST'])
def reserve():
    msg = ''
    if request.method == 'POST':
        name = request.form['name']
        contactno = request.form['contactno']
        seats = request.form['seats']
        time = request.form['time']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)



        cursor.execute("INSERT INTO register VALUES (NULL,% s, % s, % s, % s,% s)", (name,contactno,seats,time,session['id']))
        mysql.connection.commit()
        msg = 'You have successfully Reserved your seats !'

    return render_template('doreserve.html', msg = msg)
@app.route('/home')
def Index():

    return render_template('index.html')



if __name__ == '__main__':
    app.templates_auto_reload = True

    app.run()

