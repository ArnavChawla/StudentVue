import flask
from flask import Flask
import user
from flask import session, request
app = Flask(__name__)
app.secret_key = 'ImConflictedAf'
@app.route("/login", methods=["POST"])
def login():
    form = request.form
    print(request.form["username"])
    print(request.form["password"])
    student = user.user(request.form["username"],request.form["password"])
    session["username"] = request.form["username"]
    session["password"] = request.form["password"]
    return(str(student.login()))
@app.route("/classes", methods=["POST"])
def getClasses():
    student = user.user(session["username"], session["password"])
    student.login()
    return(str(student.classListThing()))

if(__name__=="__main__"):
    app.run("0.0.0.0",port=5000,debug=True)
