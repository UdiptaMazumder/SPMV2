from django.db import connection

import numpy as np

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from django.core.management import call_command

from spmapp.models import *


def getgrade(n):
    if n >= 85:
        return 4.0
    elif n >= 80:
        return 3.7
    elif n >= 75:
        return 3.3
    elif n >= 70:
        return 3.0
    elif n >= 65:
        return 2.7
    elif n >= 60:
        return 2.3
    elif n >= 55:
        return 2.0
    elif n >= 50:
        return 1.7
    elif n >= 45:
        return 1.3
    elif n >= 40:
        return 1.0
    else:
        return 0


studentlist = Student_T.objects.all()

rows=[]


for student in studentlist:

    with connection.cursor() as cursor:
            cursor.execute(''' Select sum(Marks),Credits
                            From(
                                Select c.courseID as CourseID, a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                                From spmapp_registration_t r,spmapp_section_t sc, spmapp_course_t c, spmapp_assessment_t a, spmapp_evaluation_t e
                                Where  r.student_id = '{}' and r.semester='{}' and r.year ='{}' and r.section_id = sc.sectionID and r.section_id = a.section_id
                                    and sc.course_id = c.courseID and r.registrationID = e.registration_id and e.assessment_id = a.assessmentID
                                group by  c.courseID,a.assessmentName ) d
                            group by CourseID
                             '''.format(student.studentID,"Spring",2020))

            row = cursor.fetchall()

            gpa = 0
            credits = 0

            for j in row:
                gpa+=getgrade(j[0])*j[1]
                credits+=j[1]

            rows.append((student.studentID,gpa/credits))

for k in rows:
    print(k)
print(len(rows))















