from django.db import connection
from spmapp.models import *
import numpy as np

def getgradepoint(n):
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


def getStudentWiseGpa(studentID, semester, year):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            Select sum(Marks),Credits
            From(
                SELECT c.courseID as CourseID, a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                FROM spmapp_registration_t r,
                    spmapp_section_t sc, 
                    spmapp_course_t c,
                    spmapp_assessment_t a, 
                    spmapp_evaluation_t e
                WHERE r.student_id = '{}' 
                    and r.semester='{}' 
                    and r.year ='{}' 
                    and r.section_id = sc.sectionID
                    and r.section_id = a.section_id
                    and sc.course_id = c.courseID 
                    and r.registrationID = e.registration_id and e.assessment_id = a.assessmentID
                GROUP BY  c.courseID,a.assessmentName ) DerivedTable
            GROUP BY CourseID'''.format(studentID, semester, year))

        row = cursor.fetchall()

    totalgpa = 0
    totalcredits = 0

    for j in row:
        totalgpa += getgradepoint(j[0]) * j[1]
        totalcredits += j[1]


    return semester, totalgpa / totalcredits


#studentlist = Student_T.objects.all()

#resultSpring = []

#for student in studentlist:
 #   resultSpring.append(getStudentWiseGpa(student.studentID,"Spring",2020))


#resultSummer = []

#for student in studentlist:
    #resultSummer.append(getStudentWiseGpa(student.studentID,"Summer",2020))

#resultAutumn = []

#for student in studentlist:
    #resultAutumn.append(getStudentWiseGpa(student.studentID,"Autumn",2020))

#gpas = []
#for i in range(0,len(studentlist)):
   # gpas.append((studentlist[i].studentID,resultSpring[i],resultSummer[i],resultAutumn[i]))

#for gpa in gpas:
    #print(gpa)


def getStudentWiseOverallPLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum,100*(sum( e.obtainedMarks)/sum( a.totalMarks)) as ploper
                FROM spmapp_registration_t r,
                    spmapp_assessment_t a, 
                    spmapp_evaluation_t e,
                    spmapp_co_t co, 
                    spmapp_plo_t p
                WHERE r.student_id = '{}' 
                    and  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                GROUP BY  p.ploID

                '''.format(studentID))
        row = cursor.fetchall()

    return row

def getCourseWisePLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.course_id,100*(sum(e.obtainedMarks)/derived.Total) as PLOper
               FROM spmapp_registration_t r,
                   spmapp_assessment_t a, 
                   spmapp_evaluation_t e,
                   spmapp_co_t co, 
                   spmapp_plo_t p,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM spmapp_registration_t r,
                            spmapp_assessment_t a, 
                            spmapp_evaluation_t e,
                            spmapp_co_t co, 
                            spmapp_plo_t p
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE derived.StudentID = '{}'
                    and r.student_id = derived.StudentID
                    and e.registration_id = r.registrationID
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum

               GROUP BY  p.ploID,co.course_id

               '''.format(studentID))
        row = cursor.fetchall()

    table = []
    courses = []

    for entry in row:
        if entry[1] not in courses:
            courses.append(entry[1])
    courses.sort()
    plo = ["PLO1","PLO2","PLO3","PLO4","PLO5","PLO6","PLO7","PLO8","PLO9","PLO10","PLO11","PLO12"]

    for i in courses:
        temptable = []

        for j in plo:
            found = False
            for k in row:
                if j==k[0] and i==k[1]:
                    temptable.append(np.round(k[2],2))
                    found = True
            if not found:
                temptable.append(0)
        table.append(temptable)
    return plo, courses, table


def getCOWisePLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.coNum,100*(sum(e.obtainedMarks)/derived.Total) as PLOper
               FROM spmapp_registration_t r,
                   spmapp_assessment_t a, 
                   spmapp_evaluation_t e,
                   spmapp_co_t co, 
                   spmapp_plo_t p,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM spmapp_registration_t r,
                            spmapp_assessment_t a, 
                            spmapp_evaluation_t e,
                            spmapp_co_t co, 
                            spmapp_plo_t p
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE derived.StudentID = '{}'
                    and r.student_id = derived.StudentID
                    and e.registration_id = r.registrationID
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum

               GROUP BY  p.ploID,co.coNum

               '''.format(studentID))
        row = cursor.fetchall()

    table = []
    cos = []

    for entry in row:
        if entry[1] not in cos:
            cos.append(entry[1])
    cos.sort()
    plo = ["PLO1","PLO2","PLO3","PLO4","PLO5","PLO6","PLO7","PLO8","PLO9","PLO10","PLO11","PLO12"]

    for i in cos:
        temptable = []

        for j in plo:
            found = False
            for k in row:
                if j==k[0] and i==k[1]:
                    temptable.append(np.round(k[2],2))
                    found = True
            if not found:
                temptable.append(0)
        table.append(temptable)
    return (plo,cos,table)

