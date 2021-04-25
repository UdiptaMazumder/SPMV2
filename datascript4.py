import pandas as pd
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

files = []


def updatedatabase(filename, facultyid):
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
    faculty = Faculty_T.objects.get(pk=facultyid)

    course = Course_T.objects.get(pk=data[1][2])

    sectionlist = []

    for i in sections:
        section = Section_T(SectionNum=i, CourseID=course, FacultyID=faculty, Semester="Autumn", Year=2020)
        sectionlist.append(section)

    print(len(sectionlist))

    # Registration
    reglist = []

    for i in data:
        st = Student_T.objects.get(pk=i[1])
        reg = Registration_T(StudentID=st, SectionID=sectionlist[i[3] - 1], Semester="Autumn", Year=2020)
        reglist.append(reg)

    print(len(reglist))

    # CO

    plolist = list(PLO_T.objects.all())

    colist = []

    colist.append(CO_T(CONum="CO1", CourseID=course, PLOID=plolist[1]))
    colist.append(CO_T(CONum="CO2", CourseID=course, PLOID=plolist[2]))
    colist.append(CO_T(CONum="CO3", CourseID=course, PLOID=plolist[3]))
    colist.append(CO_T(CONum="CO4", CourseID=course, PLOID=plolist[5]))

    print(len(colist))

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
            asslist.append(ass)

        for j in range(1, len(cofin) + 1):

            coid = []

            for k in colist:
                if k.CONum == comid[j - 1]:
                    coid = k
                    break
            ass = Assessment_T(AssessmentName="Final", QuestionNum=j, TotalMarks=finmarks[j - 1], COID=coid,
                               SectionID=sectionlist[i - 1], Weight=40)
            asslist.append(ass)

        coid = []

        for k in colist:
            if k.CONum == comid[j - 1]:
                coid = k
                break

        ass = Assessment_T(AssessmentName="Lab", QuestionNum=1, TotalMarks=labmark, COID=coid,
                           SectionID=sectionlist[i - 1], Weight=30)
        asslist.append(ass)

    print(len(asslist))

    # Evaluation

    evlist = []

    for i in range(0, len(data)):
        marks = data[i][5:11]
        marks.extend(data[i][13:17])
        marks.append(data[i][19])

        for j in range(0, len(marks)):
            ev = Evaluation_T(ObtainedMarks=marks[j], AssessmentID=asslist[j], RegistrationID=reglist[i])
            evlist.append(ev)

    print(len(evlist))

