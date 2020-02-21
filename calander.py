import flask,json,datetime,time
from flask import Flask,render_template,request,session


app = Flask(__name__)
app.secret_key = 'RandomStringSchedule1234502581501250123910123156'
# class schedule:
#     def __init__(self, day, times)
def convertTime(s):
    print datetime.strptime(s, '%H%M').strftime('%I:%M%p').lower()
@app.route('/today',methods=["GET","POST"])
def show():
    day = datetime.datetime.now().strftime("%Y %I:%M%p")
    time = day.split(" ")[1].lower()
    day = request.form["day"]
    if (day == "saturday" or day == "sunday"):
        return ("""{"1":"No School!"}""")
    elif (day == "monday" or day == "tuesday" or day == "friday"):
        return ("""{"Lunches":"2","1":"8:00-8:55","2":"9:00-9:50","3":"9:55-10:45","4A":"10:50-11:40","1st Lunch":"10:50-11:20","4B":"11:25-12:15","2nd Lunch":"11:45-12:15","5":"12:20-1:10","6":"1:15-2:05","7":"2:10-3:00"}""")
    elif (day == "wednesday"):
        return ("""{"Lunches":"1","2":"8:00-9:30","4":"9:35-11:05","1st Lunch":"11:10-11:20","6":"11:25-12:55"}""")
    else:
        return ("""{"Lunches":"1","1":"8:00-9:30","3":"9:35-11:05","1st Lunch":"11:10-11:50","5":"11:55-1:25","7":"1:30-3:00"}""")
    return day

app.run()
