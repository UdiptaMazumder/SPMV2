import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

# Add School
school1 = School_T(schoolID='SETS', schoolName='School of Engineering, Technology & Sciences')
school1.save()

school2 = School_T(schoolID='SBE', schoolName='School of Business and Entrepreneurship')
school2.save()

school3 = School_T(schoolID='SLASS', schoolName='School of Liberal Arts & Social Sciences')
school3.save()

#Add Department

d1 = Department_T(departmentID='CSE',departmentName='Computer Science & Engineering',school_id='SETS')
d1.save()

d2 = Department_T(departmentID='EEE',departmentName='Electrical and Electronics Engineering',school_id='SETS')
d2.save()

d3 = Department_T(departmentID='ACN',departmentName='Accounting',school_id='SBE')
d3.save()

d4 = Department_T(departmentID='MIS',departmentName='Management Information Systems',school_id='SBE')
d4.save()

d5 = Department_T(departmentID='ENG',departmentName='English',school_id='SLASS')
d5.save()

d6 = Department_T(departmentID='GSG',departmentName='Global Studies & Governance',school_id='SLASS')
d6.save()

#Add programs

p1 = Program_T(programName='B.Sc. in CSE', department_id='CSE')
p1.save()

p2 = Program_T(programName='BBA in Accounting', department_id='ACN')
p2.save()

p3 = Program_T(programName='B.Sc. in EEE', department_id='EEE')
p3.save()

p4 = Program_T(programName='BBA in MIS', department_id='MIS')
p4.save()

p5 = Program_T(programName='BA in ENG', department_id='ENG')
p5.save()

p6 = Program_T(programName='BSS in GSG', department_id='GSG')
p6.save()



# Add PLO for all programs
programList = list(Program_T.objects.all())
details = ["Knowledge", "Requirement Analysis", "Requirement Analysis", "Design", "Problem Solving", "Implementation",
           "Experiment and Analysis", "Community Engagement and Engineering", "Teamwork", "Communication",
           "Self-Motivated", "Ethics", "Process Management"]

for p in programList:
    for i in range(1, 13):
        plonum = "PLO" + str(i)
        plo = PLO_T(ploNum=plonum, program=p, details=details[i - 1])
        plo.save()

# Add Faculty Information


fnames = ["Mahady", "Sadita", "Md. Abu", "Romasa", "Mohammad Motiur", "Asif Bin", "Ferdows", "Bijoy R.", "Raihan Bin",
          "Faisal M.", "Subrata Kumar", "Mohammad Noor", "Farruk", "Sabrina", "Sanzar Adnan"]

lnames = ["Hasan", "Ahmed", "Sayed", "Qasim", "Rahman", "Khaled", "Zahid", "Arif", "Rafique", "Uddin", "Dey", "Nabi",
          "Ahmed", "Alam", "Alam"]

id = 4101

i = 0
for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="CSE")
    f.save()
    id = id + 1
    i = i + 1

fnames = ["Naheem", "Md. ", "Susmita", "Shahriar", "Kamrul", "Nabila", "Abul", "Nadim", "Farzana"]
lnames = ["Mahtab", "Saifuddin", "Mandal", "Kabir", "Islam", "Maruf", "Bashar", "Jahangir", "Chowdhury"]

id = 4201

i = 0

for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="ACN")
    f.save()
    id = id + 1
    i = i + 1



fnames = ["Shahriar", "Feroz", "Kafiul", "Abdur", "Mustafa", "Sajib", "Naziba", "Saila", "Khosru"]
lnames = ["Khan", "Ahmed", "Islam", "Razzak", "Chowdhury","Chakrabarty", "Tahsin", "Ishrat", "Salim"]

id = 4301

i = 0

for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="EEE")
    f.save()
    id = id + 1
    i = i + 1

fnames = ["Rezwanul", "Arifur Rahman", "Aminul", "Ikramul", "Bushra", "Zakia Binte"]

lnames = ["Alam", "Khan", "Islam", "Hasan", "Sanjana", "Jamal",]

id = 4401

i = 0
for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="MIS")
    f.save()
    id = id + 1
    i = i + 1

fnames = ["Shafiul", "Sara", "Vikarun", "Adilur", "Mazaharul","Mithila"]
lnames = ["Islam", "Zabeen", "Nesa", "Rahman", "Islam","Mahfuz"]

id = 4501

i = 0

for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="ENG")
    f.save()
    id = id + 1
    i = i + 1



fnames = ["Marufa", "Imtiaz", "Ahmed", "Amjad", "Mohammad", "Shahidul"]
lnames = ["Akter", "Hossain", "Taufique", "Hossain", "Hasan","Alam"]

id = 4601

i = 0

for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="GSG")
    f.save()
    id = id + 1
    i = i + 1
