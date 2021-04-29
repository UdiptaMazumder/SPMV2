import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

# Add PLO for all programs


programList = list(Program_T.objects.all())
details = ["Knowledge", "Requirement Analysis", "Requirement Analysis", "Design", "Problem Solving", "Implementation",
           "Experiment and Analysis", "Community Engagement and Engineering", "Teamwork", "Communication",
           "Self-Motivated", "Ethics", "Process Management"]

for p in programList:
    for i in range(1, 13):
        plonum="PLO"+str(i)
        plo = PLO_T(ploNum=plonum, program=p, details=details[i - 1])
        plo.save()


# Add Faculty Information


fnames = ["Mahady", "Sadita", "Md. Abu", "Romasa", "Mohammad Motiur","Asif Bin","Ferdows", "Bijoy R.", "Raihan Bin", "Faisal M.",
          "Subrata Kumar", "Mohammad Noor", "Farruk", "Sabrina", "Sanzar Adnan"]

lnames = ["Hasan", "Ahmed", "Sayed", "Qasim","Rahman","Khaled", "Zahid", "Arif", "Rafique", "Uddin",  "Dey", "Nabi",
          "Ahmed", "Alam", "Alam"]

id = 4250

i = 0
for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="CSE")
    f.save()
    id = id + 1
    i = i + 1


fnames = [ "Naheem", "Md. ", "Susmita", "Shahriar", "Kamrul","Nabila", "Abul", "Nadim", "Farzana"]
lnames = ["Mahtab","Saifuddin","Mandal","Kabir", "Islam","Maruf","Bashar","Jahangir","Chowdhury"]

id =4201

i=0

for name in fnames:
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department_id="ACN")
    f.save()
    id = id + 1
    i = i + 1
