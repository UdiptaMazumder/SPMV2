import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

# Add School
school1 = School_T(schoolID='SLASS', schoolName='School of Liberal Arts & Social Sciences')
school1.save()

#Add Department

d1 = Department_T(departmentID='MIS',departmentName='Management Information Systems',school_id='SBE')
d1.save()

d2 = Department_T(departmentID='ENG',departmentName='English',school_id='SLASS')
d2.save()

d3 = Department_T(departmentID='GSG',departmentName='Global Studies & Governance',school_id='SLASS')
d3.save()

#Add programs

p1 = Program_T(programName='BBA in MIS', department_id='MIS')
p1.save()

p2 = Program_T(programName='BA in ENG', department_id='ENG')
p2.save()

p3 = Program_T(programName='BSS in GSG', department_id='GSG')
p3.save()



# Add PLO for all programs
programList = []
programList.append(p1)
programList.append(p2)
programList.append(p3)

details = ["Knowledge", "Requirement Analysis", "Requirement Analysis", "Design", "Problem Solving", "Implementation",
           "Experiment and Analysis", "Community Engagement and Engineering", "Teamwork", "Communication",
           "Self-Motivated", "Ethics", "Process Management"]

for p in programList:
    for i in range(1, 13):
        plonum = "PLO" + str(i)
        plo = PLO_T(ploNum=plonum, program=p, details=details[i - 1])
        plo.save()

# Add Faculty Information


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
