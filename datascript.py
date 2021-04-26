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

# for p in programList:
#  for i in range(1, 14):
#     plonum="PLO"+str(i)

#    plo = PLO_T(ploNum=plonum, program=p, details=details[i - 1])
#   plo.save()


# Add Faculty Information


#fnames = ["Mahady", "Sadita", "Md. Abu", "Romasa", "Ferdows", "Bijoy R.", "Mohammad Motiur", "Raihan Bin", "Faisal M.",
          #"Asif Bin", "Subrata Kumar", "Mohammad Noor", "Farruk", "Sabrina", "Sanzar Adnan"]

#lnames = ["Hasan", "Ahmed", "Sayed", "Qasim", "Zahid", "Arif", "Rahman", "Rafique", "Uddin", "Khaled", "Dey", "Nabi",
          #"Ahmed", "Alam", "Alam"]

#id = 4250

#i = 0

id =4201

i=0

fnames = [ "Naheem", "Md. ", "Susmita", "Shahriar", "Kamrul","Nabila", "Abul", "Nadim", "Farzana"]
lnames = ["Mahtab","Saifuddin","Mandal","Kabir", "Islam","Maruf","Bashar","Jahangir","Chowdhury"]

for name in fnames:
    d = Department_T.objects.get(pk="BBA")
    f = Faculty_T(facultyID=id, firstName=name, lastName=lnames[i], employeeType="F", department=d)
    f.save()
    id = id + 1
    i = i + 1
