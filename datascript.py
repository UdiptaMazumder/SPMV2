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
    for i in range(1, 14):
        plo = PLO_T(PLONum=i, ProgramID=p, Details=details[i - 1])
        plo.save()



# Add Faculty Information


filename = ["CSE101.xlsx", "CSE104.xlsx", "CSE201.xlsx", "CSE203.xlsx", "CSE204.xlsx", "CSE210.xlsx", "CSE211.xlsx",
            "CSE213.xlsx", "CSE214.xlsx", "CSE216.xlsx", "CSE303.xlsx", "CSE307.xlsx", "CSE309.xlsx"]

df = pd.read_excel(filename[0], sheet_name="Marks")

data = df.values.tolist()

# comid = data[0][5:11]
# cofin = data[0][13:17]
# colab = data[0][19]

# midfull = data[2][5:11]
# finfull = data[2][13:17]
# labful = data[2][19]


fnames = ["Mahady", "Sadita", "Md. Abu", "Romasa", "Ferdows",
"Bijoy R.", "Mohammad Motiur", "Raihan Bin", "Faisal M.", "Asif Bin", "Subrata Kumar", "Mohammad Noor",
 "Farruk", "Sabrina", "Sanzar Adnan"]

lnames = ["Hasan", "Ahmed", "Sayed", "Qasim", "Zahid", "Arif", "Rahman", "Rafique", "Uddin", "Khaled", "Dey", "Nabi",
    "Ahmed", "Alam", "Alam"]

id = 4250

i = 0

for name in fnames:
    d=Department_T.objects.get(pk="CSE")
    f = Faculty_T(FacultyID=id, FirstName=name, LastName=lnames[i], EmployeeType="F", DepartmentID=d)
    f.save()
    id=id+1
    i=i+1
