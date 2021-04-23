import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

files = ["CSE101.xlsx", "CSE104.xlsx", "CSE201.xlsx", "CSE203.xlsx", "CSE204.xlsx", "CSE210.xlsx", "CSE211.xlsx",
         "CSE213.xlsx", "CSE214.xlsx", "CSE216.xlsx", "CSE303.xlsx", "CSE307.xlsx", "CSE309.xlsx"]



def updatedatabase(filename, faculties):
    df = pd.read_excel(filename, sheet_name="Marks")

    data = df.values.tolist()

    comid = data[0][5:11]
    cofin = data[0][13:17]
    colab = data[0][19]

    midmarks = data[2][5:11]
    finmarks = data[2][13:17]
    labmark = data[2][19]

    data = data[3:][:]

    for i in data:
        i[1] = int(i[1])
        i[3] = int(int(i[3]))

    currentstudents = list(Student_T.objects.all())
    newstudents=[]

    sections = []

    for i in data:
        if i[1] not in currentstudents:
            newstudents.append(i[1])

        if i[3] not in sections:
            sections.append(i[3])















faculties = 2

updatedatabase(files[0],faculties)




