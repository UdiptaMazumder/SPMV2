import pandas as pd
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

files = ["CSE210.xlsx", "CSE214.xlsx", "CSE216.xlsx"]

faculties =[]
faculties.append(Faculty_T.objects.get(pk=4254))
faculties.append(Faculty_T.objects.get(pk=4255))
faculties.append(Faculty_T.objects.get(pk=4257))


def updatedatabase(filename, d, semester):
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
        i[1] = int(i[1]) + d
        i[3] = int(int(i[3]))

    currentstudents = list(Student_T.objects.all())
    newstudents = []

    sections = []

    for i in data:
        if i[1] not in currentstudents:
            newstudents.append(i[1])

        if i[3] not in sections:
            sections.append(i[3])

    # Students

    dept = Department_T.objects.get(pk="CSE")
    program = Program_T.objects.get(pk=1)

    for i in newstudents:
        student = Student_T(StudentID=i, DepartmentID=dept, ProgramID=program)
        student.save()

    # Sections

    course = Course_T.objects.get(pk=data[1][2])

    sectionlist = []

    for i in sections:
        faculty = faculties[i - 1]
        section = Section_T(SectionNum=i, CourseID=course, FacultyID=faculty, Semester=semester, Year=2020)
        section.save()
        sectionlist.append(section)

    # Registration
    reglist = []

    for i in data:
        st = Student_T.objects.get(pk=i[1])
        reg = Registration_T(StudentID=st, SectionID=sectionlist[i[3] - 1], Semester=semester, Year=2020)
        reg.save()
        reglist.append(reg)

    # CO

    plolist = list(PLO_T.objects.filter(ProgramID=1))


    colist = []

    colist.append(CO_T(CONum="CO1", CourseID=course, PLOID=plolist[0]))
    colist.append(CO_T(CONum="CO2", CourseID=course, PLOID=plolist[1]))
    colist.append(CO_T(CONum="CO3", CourseID=course, PLOID=plolist[2]))
    colist.append(CO_T(CONum="CO4", CourseID=course, PLOID=plolist[3]))

    colist[0].save()
    colist[1].save()
    colist[2].save()
    colist[3].save()



    # Assessment
    asslist = []
    for i in range(1, len(sectionlist) + 1):
        for j in range(1, len(comid) + 1):

            coid = []

            for k in colist:
                if k.CONum == comid[j - 1]:
                    coid = k
                    break

            ass = Assessment_T(AssessmentName="Mid", QuestionNum=j, TotalMarks=midmarks[j - 1], COID=coid,
                               SectionID=sectionlist[i - 1], Weight=30)
            ass.save()
            asslist.append(ass)

        for j in range(1, len(cofin) + 1):

            coid = []

            for k in colist:
                if k.CONum == comid[j - 1]:
                    coid = k
                    break
            ass = Assessment_T(AssessmentName="Final", QuestionNum=j, TotalMarks=finmarks[j - 1], COID=coid,
                               SectionID=sectionlist[i - 1], Weight=40)

            ass.save()
            asslist.append(ass)

        coid = []

        for k in colist:
            if k.CONum == comid[j - 1]:
                coid = k
                break

        ass = Assessment_T(AssessmentName="Lab", QuestionNum=1, TotalMarks=labmark, COID=coid,
                           SectionID=sectionlist[i - 1], Weight=30)
        ass.save()
        asslist.append(ass)

    # Evaluation

    evlist = []

    for i in range(0, len(data)):
        marks = data[i][5:11]
        marks.extend(data[i][13:17])
        marks.append(data[i][19])

        for j in range(0, len(marks)):
            ev = Evaluation_T(ObtainedMarks=marks[j], AssessmentID=asslist[j], RegistrationID=reglist[i])
            ev.save()
            evlist.append(ev)


for file in files:
    updatedatabase(file, 2, "Spring")
    updatedatabase(file, 0, "Summer")
    updatedatabase(file, 1, "Autumn")