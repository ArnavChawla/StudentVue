r = session.get("https://wa-bsd405.edupoint.com/LoginSub.aspx")
bs = soup(r.text,"html.parser")
schools = bs.findAll("option")
print(schools)
codeting= ""
print(school)
for schol in schools:
    if (str(schol.get_text()).strip() == str(school).strip()):
        print(codeting)
        codeting = schol["value"]
data = {
    "curSchoolOrgYearGU": codeting
}
r = session.post("https://wa-bsd405.edupoint.com/Service/SubLogin.asmx/LoadSubs",data=data)
print(r.text)
bs = soup(r.text,"xml")
names = bs.findAll("Name")
names.pop(0)
dict = []
for name in names:
    dict.append(name.get_text())
print(dict)
for teacher in teachers:
    for ting in dict:
        if teacher in ting:
            print(teacher)
