#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Assignment 13

import sys
import sqlite3
from flask import Flask, render_template, request, session, redirect, g, flash

#sys.path.append("")

username = "admin"
password = "password"
DATABASE = 'hw13'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()




@app.route('/')
def landing():
    error = None
    return render_template('login.html')


@app.route('/login', methods = ['GET', 'POST']) 
def login():
    error = None
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['logged_in'] = True
            return redirect('/dashboard')
        else:
            flash('Invalid login')
            return render_template('login.html', error = error)
            
            



@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if session['logged_in'] == True:
        cur = get_db().cursor()
        cur.execute('select ID, FIRSTNAME, LASTNAME from STUDENTS')
        s_list = [dict(id = row[0], firstname = row[1], lastname = row[2]) for row in cur.fetchall()]
        cur.execute('select ID, SUBJECT, NUM_QUESTIONS, DATE_QUIZ from QUIZZES')
        q_list = [dict(id = row[0], subject = row[1], num_questions = row[2], date_quiz = row[3]) for row in cur.fetchall()]
        return render_template("dashboard.html", s_list = s_list, q_list = q_list)
    else:
        return redirect('/')

    
@app.route('/student/add', methods = ['GET','POST'])
def addstudent():
    if session['logged_in'] == True:
        if request.method == 'GET':
            return render_template("addstudent.html")
        elif request.method == 'POST':
                cur = get_db().cursor()
                cur.execute('insert into STUDENTS (FIRSTNAME, LASTNAME) values (?,?)',(request.form['firstname'], request.form['lastname']))
                get_db().commit()
                return redirect('/dashboard')
        else:
            flash("Error adding data")
            return redirect('/student/add')
    else:
        return redirect('/login')


@app.route('/quiz/add', methods = ['GET','POST'])
def addquiz():
    if session['logged_in'] == True:
        if request.method == 'GET':
            return render_template("addquiz.html")
        elif request.method == 'POST':
                cur = get_db().cursor()
                cur.execute('insert into QUIZZES (SUBJECT, NUM_QUESTIONS, DATE_QUIZ) values (?,?,?)',(request.form['subject'],request.form['numquestions'],request.form['quizdate']))
                get_db().commit()
                return redirect('/dashboard')
        else:
            flash("Error adding data")
            return redirect('/quiz/add')
    else:
        return redirect('/login')


@app.route('/student/<id>', methods = ['GET'])
def viewresult(id):
    if session['logged_in'] == True:
        cur = get_db().cursor()
        cur.execute('select FIRSTNAME, LASTNAME from STUDENTS where ID = ?',(id))
        s_name = [dict(firstname = row[0], lastname = row[1]) for row in cur.fetchall()]
        cur.execute('select QUIZ_ID, SCORE from RESULTS where STUDENT_ID = ?', (id))
        s_views = [dict(quiz_id = row[0], score = row[1]) for row in cur.fetchall()]
        return render_template('viewresults.html', s_name = s_name, s_views = s_views)
    
    else:
        return redirect('/login')
        
        

@app.route('/results/add', methods = ['GET','POST'])
def addresult():
    if session['logged_in'] == True:
        cur = get_db().cursor()
        if request.method == 'GET':
            cur.execute('select ID, FIRSTNAME, LASTNAME from STUDENTS')
            s_list = [dict(id = row[0], fullname = row[1] + " " + row[2]) for row in cur.fetchall()]
            cur.execute('select ID, SUBJECT from QUIZZES')
            q_list = [dict(id = row[0], subject = row[1]) for row in cur.fetchall()]
            return render_template('addresult.html', s_list = s_list, q_list = q_list)
        else:
            if request.method == 'POST':
                cur.execute('insert into RESULTS (STUDENT_ID, QUIZ_ID, SCORE) values (?, ?, ?)', (request.form['students'], request.form['quiz'], request.form['gradescore']))
                get_db().commit()
                return redirect("/dashboard")
    else:
        return redirect('/login')
    
    
    

if __name__ == '__main__':
    app.secret_key = 'xa8mf84fs655yl14'
    app.run()


# In[ ]:





# In[ ]:




