# -*- coding: utf-8 -*-
import flask
from flask import Flask,session
from user import user
from flask import request,redirect,url_for,render_template
import json,datetime
import hashlib
from itsdangerous import URLSafeTimedSerializer
from flask.sessions import TaggedJSONSerializer
app = Flask(__name__)
dates=[]
app.secret_key = 'Bsd405GradebookCas'

@app.route("/login", methods=["POST"])
def login():
    form = request.form
    session['username'] = str(request.form['username'])
    session['password'] = str(request.form['password'])
    #student = user(session['username'],session['password'])
    return redirect(url_for('number',username=request.form['username'],password=request.form['password']),code=307)

@app.route('/get_number',methods=["GET","POST"])
def number():
    student = user(request.args.get('username'),request.args.get('password'))
    name = student.login()
    dictionary  = {'session': request.cookies.get('session') }
    data ={}
    data.update(dict(student.classListThing()))
    data.update(dictionary)
    print(data)
    data["name"]= name
    return str(json.dumps(data))
@app.route("/get_weight",methods=["POST"])
def get_weight():
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer('Bsd405GradebookCas', salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    newdict = s.loads(request.form['session'])
    student = user(newdict['username'],newdict['password'])
    student.login()
    id = request.form['id']
    return(json.dumps(student.getClassWeighting(id)))
@app.route("/assignment_data",methods=["POST"])
def get_assignment():
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer('Bsd405GradebookCas', salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    newdict = s.loads(request.form['session'])
    student = user(newdict['username'],newdict['password'])
    student.login()
    id = request.form['id']
    return(student.getClassAssignemnts(id))
@app.route('/today',methods=["GET","POST"])
def show():
    day = datetime.datetime.now().strftime("%Y %I:%M%p")
    time = day.split(" ")[1].lower()
    ogdate = request.form["date"]
    year, month, days = (int(x) for x in ogdate.split('-'))
    print("{},{},{}".format(year,month,days))
    day = datetime.date(year, month, days).weekday()
    daydict = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    day =daydict[day]
    print(day)
    for date in dates:
        #print date
        json.loads(date)["date"]
        if(json.loads(date)["date"]==ogdate):
            return date
    if (day == "saturday" or day == "sunday"):
        return ("""{"1":"No School!"}""")
    elif (day == "monday" or day == "tuesday" or day == "friday"):
        return ("""{"Lunches":"2","1":"8:00-8:55","2":"9:00-9:50","3":"9:55-10:45","4A":"10:50-11:40","1st Lunch":"10:50-11:20","4B":"11:25-12:15","2nd Lunch":"11:45-12:15","5":"12:20-1:10","6":"1:15-2:05","7":"2:10-3:00"}""")
    elif (day == "wednesday"):
        return ("""{"Lunches":"1","2":"8:00-9:30","4":"9:35-11:05","1st Lunch":"11:10-11:20","6":"11:25-12:55"}""")
    else:
        return ("""{"Lunches":"1","1":"8:00-9:30","3":"9:35-11:05","1st Lunch":"11:10-11:50","5":"11:55-1:25","7":"1:30-3:00"}""")
    return day
@app.route("/print",methods=["POST"])
def thing():
    return (str(session.get('username')))
@app.route('/student_data',methods=["POST"])
def data():
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer('Bsd405GradebookCas', salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    newdict = s.loads(request.form['session'])
    student = user(newdict['username'],newdict['password'])
    student.login()
    return student.studentName
@app.route('/set_calendar')
def set():
    return render_template('set.html')

@app.route('/set',methods=["POST","GET"])

def look():
    if(request.method=="POST"):
        dates.append(json.dumps((request.form)))
        print(dates)
    else:
        pass
    return str(dates)
if __name__ == '__main__':
    app.run("0.0.0.0",port="5000")
