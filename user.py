import requests
from bs4 import BeautifulSoup as soup
import json
import sys
from imp import reload
class gradePeriod:
    def __init__(self, name, id):
            self.term = name
            self.id = id
class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.teachers = []
        self.letterGrades =[]
        self.numberGrades = []
        self.classids = []
        self.session = requests.Session()
        self.idNumber = ""

    def login(self):

        url = "https://wa-bsd405-psv.edupoint.com/PXP2_Login_Student.aspx?regenerateSessionId=True"
        r = self.session.get(url)
        bs = soup(r.text, "html.parser")
        view = bs.find("input",{"name":"__VIEWSTATE"})["value"]
        generator = bs.find("input",{"name":"__VIEWSTATEGENERATOR"})["value"]
        validation = bs.find("input", {"name":"__EVENTVALIDATION"})["value"]

        loginPayload = {
            "__VIEWSTATE":view,
            "__VIEWSTATEGENERATOR":generator,
            "__EVENTVALIDATION":validation,
            "ctl00$MainContent$username": self.username,
            "ctl00$MainContent$password": self.password
        }
        r = self.session.post(url,data=loginPayload)
        bs = soup(r.text, "html.parser")

        self.studentName = str(bs.find("span",{"id":"Greeting"})).split(', ')[1].split(',')[0]
        print(self.studentName)
        toNavigate = bs.findAll("a",{"class":"list-group-item"})[7]["href"]
        print(toNavigate)
        r = self.session.get("https://wa-bsd405-psv.edupoint.com/{}".format(toNavigate))
        bs = soup(r.text, "html.parser")
        userdata = json.loads(str(bs.find("button",{"class":"btn btn-link course-title"})["data-focus"]))
        self.idNumber = userdata["FocusArgs"]["studentGU"]
        self.schoolNumber = userdata["FocusArgs"]["schoolID"]
        self.gradePeriodGU = userdata["FocusArgs"]["gradePeriodGU"]
        self.OrgYearGU = userdata["FocusArgs"]["OrgYearGU"]
        self.school = bs.find("div",{"class":"school"}).get_text()
        self.getTeachers()
        self.getGrades()
        self.getQuarters()
        self.class_ids()
        self.getClassNames()
        self.getRoomNumber()
        return self.studentName
    def getQuarters(self):
        r = self.session.get("https://wa-bsd405-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU={}".format(self.idNumber))
        bs = soup(r.text, "html.parser")
        self.quarters = []
        for data in bs.findAll("a",{"data-action":"GB.SetTerm"}):
            self.quarters.append(gradePeriod(data.get_text().lstrip(),data["data-period-id"]))
    def getTeachers(self):
        r = self.session.get("https://wa-bsd405-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU={}".format(self.idNumber))
        bs = soup(r.text, "html.parser")
        teachers = []
        for item in bs.findAll("div",{"class":"teacher hide-for-screen"}):
            self.teachers.append(item.text)
        newteachers = []
        for teacher in self.teachers:
            first = teacher.split(" ")[0]
            last = teacher.split(" ")[1]
            newteachers.append("{}, {}".format(last, first))
        self.teachers= newteachers
        return(self.teachers)
    def getClassNames(self):
        r = self.session.get("https://wa-bsd405-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU={}".format(self.idNumber))
        bs = soup(r.text, "html.parser")
        self.classNames = []
        for item in bs.findAll("button",{"class":"btn btn-link course-title"}):
            self.classNames.append(item.text)
        return(self.classNames)
    def getRoomNumber(self):
        r = self.session.get("https://wa-bsd405-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU={}".format(self.idNumber))
        bs = soup(r.text, "html.parser")
        self.roomNumbers = []
        for item in bs.findAll("div",{"class":"teacher-room hide-for-print"}):
            self.roomNumbers.append(item.text)
        return(self.roomNumbers)
    def getGrades(self):
        r = self.session.get("https://wa-bsd405-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU={}".format(self.idNumber))
        bs = soup(r.text, "html.parser")
        bs1 = soup(str((bs.find("tbody"))),"html.parser")
        numbergrade = []
        for item in bs1.findAll("span",{"class":"score"}):
            print(item.get_text())
            self.numberGrades.append(item.get_text())
        for item in bs1.findAll("span",{"class":"mark"}):
            print(item.get_text())
            self.letterGrades.append(item.get_text())
    def check_subs(self):
      print(self.teachers)
      r = self.session.get("https://wa-bsd405.edupoint.com/LoginSub.aspx")
      bs = soup(r.text,"html.parser")
      schools = bs.findAll("option")
      codeting= ""
      for schol in schools:
          if (str(schol.get_text()).strip() == str(self.school).strip()):
              codeting = schol["value"]
      data = {
          "curSchoolOrgYearGU": codeting
      }
      r = self.session.post("https://wa-bsd405.edupoint.com/Service/SubLogin.asmx/LoadSubs",data=data)
      bs = soup(r.text,"xml")
      names = bs.findAll("Name")
      names.pop(0)
      dict = []
      for name in names:
          dict.append(name.get_text())
      print(dict)
      for teacher in self.teachers:
          for ting in dict:
              if teacher in ting:
                if teacher != "None":
                    print(teacher)
    def class_ids(self):
        r = self.session.get("https://wa-bsd405-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0&studentGU={}".format(self.idNumber))
        bs = soup(r.text, "html.parser")
        bs1 = soup(str((bs.find("tbody"))),"html.parser")
        temp = []
        for item in bs1.findAll("tr"):
            classcode = str(item).split("data-guid=\"")[1].split("\"")[0]
            temp.append(classcode)
        for item in temp:
            if item not in self.classids:
                self.classids.append(item)
    def classListThing(self):
        i = 0
        full = {"students":[]}
        for i in range(0,len(self.classids)):
            data = {"{}".format(i):{"name": "{}".format(self.classNames[i]),"numberGrade":"{}".format(self.numberGrades[i]), "letterGrade":"{}".format(self.letterGrades[i]), "classId":"{}".format(self.classids[i]), "teacher":"{}".format(self.teachers[i]), "room":"{}".format(self.roomNumbers[i].split(": ")[1])}}
            print(data)
            full["students"].append(data)
            i+=1
        return(full)


    def getClassAssignemnts(self, id):
        data ={"request":{"control":"Gradebook_ClassDetails","parameters":{"schoolID":int(self.schoolNumber),"classID":int(id),"gradePeriodGU":self.gradePeriodGU, "subjectID":-1,"teacherID":-1,"assignmentID":-1,"studentGU":self.idNumber,"AGU":"0","OrgYearGU":self.OrgYearGU}}}
        r= self.session.post("https://wa-bsd405-psv.edupoint.com/service/PXP2Communication.asmx/LoadControl",json=data)
        class_information = r.json()['d']['Data']['html']
        start = class_information.index('"dataSource"')
        end = class_information[start:].index("}]")
        assignment_data = json.loads("{" + class_information[start: start + end] + "}]}")
        return  (json.dumps(assignment_data))

    def getClassWeighting(self, id):
        data ={"request":{"control":"Gradebook_ClassDetails","parameters":{"schoolID":int(self.schoolNumber),"classID":int(id),"gradePeriodGU":self.gradePeriodGU, "subjectID":-1,"teacherID":-1,"assignmentID":-1,"studentGU":self.idNumber,"AGU":"0","OrgYearGU":self.OrgYearGU}}}
        r= self.session.post("https://wa-bsd405-psv.edupoint.com/service/PXP2Communication.asmx/LoadControl",json=data)
        class_information = r.json()['d']['Data']['html']
        start = class_information.index('"dataSource"')
        end = class_information[start:].index("}]")
        # assignment_data = json.loads("{" + class_information[start: start + end] + "}]}")
        # print (json.dumps(assignment_data))
        categories = {}

        try:
            start = class_information.index("data-data-source=")
            end = class_information.index('>', start)

            category_data = json.loads(class_information[start + len("data-data-source=") + 1 : end - 1].replace("&quot;", '"'))

            for category in category_data:
                categories[category.get("Category")] = {
                    "percentage" : float(category.get("PctOfGrade"))
                }
            return(categories)
        except:
            return """{"weight":"no weighting"}"""
