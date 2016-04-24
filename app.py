import os
from flask import Flask, render_template, request, \
                    url_for, request, session, flash, redirect, g
from functools import wraps
import sqlite3
import uuid

app = Flask(__name__)
app.database = 'users.db'

app.secret_key = "secret_session_key"


class session_info:
    user = ""

def login_required(f):
    @wraps(f)
    def frp(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You Must Login First!')
            return redirect(url_for('login'))
    return frp

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
c = session_info()
@app.route("/")
def index():
    
    session['logged_in'] = False
    return redirect(url_for('login'))
    #return render_template("login.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #if request.form['username'] != 'admin' \
        #    or request.form['password'] != 'admin':
        g.db = connect_db()
        cur = g.db.execute('select * from users')
        names = [dict(user=row[0], password=row[1]) for row in cur.fetchall()]
        flag = 0
        for u,p in names.items():
            if(request.form['username'] == u and request.form['password'] == p):
                flag = 1
        if(flag == 0):
            error = 'Invalid login credentials. Please Try Again'
        else:
            session['logged_in'] = True
            
            c.user = request.form['username']
            for v,w in session.items():
                print(v,": ",w)

            return render_template("upload.html")
            return redirect(url_for('.upload'))
    return render_template('login.html', error = error)

@app.route("/upload", methods=['POST', 'GET'])
@login_required

def upload():
    if(session['logged_in'] == True):
        

        
        target = os.path.join(APP_ROOT, 'uploads/'+ getattr(c, 'user'))
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file[]"):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

        return render_template("complete.html")
    else:
        return("login first!!")

def connect_db():
    sqlite3.connect(app.database)

if __name__ == "__main__":
    app.run(port=4555, debug=True)