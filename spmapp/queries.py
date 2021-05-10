from django.db import connection
from spmapp.models import *
import numpy as np

studentlist = Student_T.objects.all()

programlist = Program_T.objects.all()


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


def getStudentWiseGPA(studentID, semester, year):
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

    return np.round(totalgpa / totalcredits, 2)


def getSchoolWiseGPA(school, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT st.studentID
            FROM spmapp_school_t s,
                spmapp_department_t d,
                spmapp_student_t st
            WHERE s.schoolID = d.school_id
                and d.departmentID = st.department_id
                and s.schoolID = '{}'
            '''.format(school))

        studentlist = cursor.fetchall()

    totalgpa = 0.0
    totalstudent = 0

    for st in studentlist:
        totalgpa += getStudentWiseGPA(st[0], semester, year)
        totalstudent += 1

    return totalgpa / totalstudent


def getDeptWiseGPA(dept, semester, year):
    totalgpa = 0.0
    totalstudent = 0

    for st in studentlist:
        if st.department_id == dept:
            totalgpa += getStudentWiseGPA(st.studentID, semester, year)
            totalstudent += 1

    return totalgpa / totalstudent


def getProgramWiseGPA(program, semester, year):
    totalgpa = 0.0
    totalstudent = 0

    for st in studentlist:
        if st.program_id == program:
            totalgpa += getStudentWiseGPA(st.studentID, semester, year)
            totalstudent += 1

    return totalgpa / totalstudent


# studentlist = Student_T.objects.all()

# resultSpring = []

# for student in studentlist:
#   resultSpring.append(getStudentWiseGpa(student.studentID,"Spring",2020))


# resultSummer = []

# for student in studentlist:
# resultSummer.append(getStudentWiseGpa(student.studentID,"Summer",2020))

# resultAutumn = []

# for student in studentlist:
# resultAutumn.append(getStudentWiseGpa(student.studentID,"Autumn",2020))

# gpas = []
# for i in range(0,len(studentlist)):
# gpas.append((studentlist[i].studentID,resultSpring[i],resultSummer[i],resultAutumn[i]))

# for gpa in gpas:
# print(gpa)


def getStudentWiseOverallPLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum as plonum,100*(sum( e.obtainedMarks)/sum( a.totalMarks)) as plopercent
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


def getCourseWisePLO(studentID, cat):
    with connection.cursor() as cursor:
        cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.course_id,sum(e.obtainedMarks),sum(a.totalMarks), derived.Total
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
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6", "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in courses:
        temptable = []
        if cat == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if cat == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif cat == 'chart':
                        temptable.append(np.round(100 * k[2] / k[4], 2))
                    found = True
            if not found:
                if cat == 'report':
                    temptable.append('N/A')
                elif cat == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, courses, table


def getCOWisePLO(studentID, cat):
    with connection.cursor() as cursor:
        cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.coNum, sum(e.obtainedMarks),sum(a.totalMarks),derived.Total 
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
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6", "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in cos:
        temptable = []
        if cat == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if cat == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif cat == 'chart':
                        temptable.append(np.round(100 * k[2] / k[4], 2))
                    found = True
            if not found:
                if cat == 'report':
                    temptable.append('N/A')
                elif cat == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, cos, table


def getDeptWisePLO(dept):
    with connection.cursor() as cursor:
        cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_student_t st,
                    spmapp_department_t d,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE r.student_id = st.studentID
                    and st.department_id = d.departmentID
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.department_id = '{}'
                    GROUP BY p.ploID,r.student_id) derived
             GROUP BY derived.ploNum
                   '''.format(dept))
        row = cursor.fetchall()
    return row


def getProgramWiseOverallPLO(program):
    with connection.cursor() as cursor:
        cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_student_t st,
                    spmapp_program_t p,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE r.student_id = st.studentID
                    and st.program_id = p.programID
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and st.department_id = '{}'
                    GROUP BY p.ploID,r.student_id) derived
             GROUP BY derived.ploNum
                   '''.format(program))
        row = cursor.fetchall()
    return row


def getSchoolWisePLO(school):
    with connection.cursor() as cursor:
        cursor.execute('''
             SELECT derived.plonum, avg(per)
             FROM(
                SELECT p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_student_t st,
                    spmapp_department_t d,
                    spmapp_school_t s,
                    spmapp_assessment_t a,
                    spmapp_co_t c,
                    spmapp_plo_t p
                WHERE r.student_id = st.studentID
                    and st.department_id = d.departmentID
                    and d.school_id = s.scholID
                    and e.registration_id = r.registrationID
                    and a.assessmentID = e.assessment_id
                    and a.co_id = c.coID
                    and c.plo_id = p.ploID
                    and d.school_id = '{}'
                    GROUP BY p.ploID,r.student_id) derived
             GROUP BY derived.ploNum
                   '''.format(school))
        row = cursor.fetchall()
    return row


def getSchoolWiseEnrolledStudents(school, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT count( distinct st.studentID)
            FROM spmapp_school_t s,
                spmapp_department_t d,
                spmapp_student_t st,
                spmapp_registration_t r
            WHERE r.student_id = st.studentID
                and st.department_id = d.departmentID
                and d.school_id = s.schoolID
                and r.semester = '{}'
                and r.year = '{}'
                and s.schoolID = '{}'
            '''.format(semester, year, school))
        row = cursor.fetchall()

    return row[0][0]


def getDeptWiseEnrolledStudents(dept, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT count(distinct st.studentID)
            FROM spmapp_department_t d,
                spmapp_student_t st,
                spmapp_registration_t r
            WHERE r.student_id = st.studentID
                and r.semester = '{}'
                and r.year = '{}'
                and st.department_id = '{}'
            '''.format(semester, year, dept))
        row = cursor.fetchall()

    return row[0][0]


def getProgramWiseEnrolledStudents(program, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT count( distinct st.studentID)
            FROM spmapp_program_t p,
                spmapp_student_t st,
                spmapp_registration_t r
            WHERE r.student_id = st.studentID
                and st.program_id = p.programID
                and r.semester = '{}'
                and r.year = '{}'
                and st.program_id = '{}'
            '''.format(semester, year, program))
        row = cursor.fetchall()
    return row[0][0]


def getAllSemesters():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT semester, year
            FROM spmapp_registration_t r
            
        ''')

        row = cursor.fetchall()
    return row


def getProgramWisePLO(program):
    plo = ['PLO1', 'PLO2', 'PLO3', 'PLO4', 'PLO5', 'PLO6', 'PLO7', 'PLO8', 'PLO9', 'PLO10', 'PLO11', 'PLO12']
    achieved = []
    attempted = []

    for p in plo:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT(*)
                FROM(SELECT AVG(percourse) as actual
                    FROM (SELECT r.student_id as StudentID, sum(e.obtainedMarks)/sum(a.totalMarks) as percourse
                        FROM spmapp_registration_t r,
                            spmapp_evaluation_t e,
                            spmapp_assessment_t a,
                            spmapp_co_t c,
                            spmapp_plo_t p,
                            spmapp_program_t pr
                        WHERE r.registrationID = e.registration_id
                            and e.assessment_id = a.assessmentID
                            and a.co_id = c.coID
                            and c.plo_id = p.ploID
                            and p.program_id = pr.programID
                            and pr.programID='{}'
                        GROUP BY r.student_id,c.coID) per
                    GROUP BY per.StudentID) avgTable
          '''.format(program))
            row = cursor.fetchall()

            if row is not None:
                attempted.append(row[0][0])
            else:
                attempted.append(0)

    for p in plo:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT(*)
               FROM(
                SELECT StudentID, AVG(percourse) as actual
                FROM(
                           SELECT r.student_id as StudentID, 100*sum(e.obtainedMarks)/sum(a.totalMarks) as percourse
                               FROM spmapp_registration_t r,
                                   spmapp_evaluation_t e,
                                   spmapp_assessment_t a,
                                   spmapp_co_t c,
                                   spmapp_plo_t p,
                                   spmapp_program_t pr
                               WHERE r.registrationID = e.registration_id
                                   and e.assessment_id = a.assessmentID
                                   and a.co_id = c.coID
                                   and c.plo_id = p.ploID
                                   and p.program_id = pr.programID
                                   and pr.programID='{}'
                                   and p.ploNum ='{}'
                               GROUP BY r.student_id,r.registrationID) d1
                           GROUP BY StudentID)d2
                           WHERE actual>=40
               '''.format(program, p))
            row = cursor.fetchall()

            if row is not None:
                achieved.append(row[0][0])
            else:
                achieved.append(0)

    return plo, achieved, attempted


def getVerdictTable(course):
    row = []
    total = 0
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT coNum, ploNum, COUNT(marks)
               FROM(
                       SELECT c.coNum as coNum,p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                       FROM spmapp_registration_t r,
                           spmapp_evaluation_t e,
                           spmapp_assessment_t a, 
                           spmapp_co_t c,
                           spmapp_plo_t p
                       WHERE r.registrationID = e.registration_id
                           and e.assessment_id = a.assessmentID
                           and a.co_id = c.coID
                           and c.plo_id = p.ploID
                            and c.course_id = '{}'
                       GROUP BY r.student_id,c.course_id,c.coID, p.ploID
                       )derived

               WHERE marks>=40
               GROUP BY coNum,ploNum

               '''.format(course))
        row = cursor.fetchall()
        if row is None:
            row = []



    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT coNum, ploNum, COUNT(marks)
               FROM(
                       SELECT r.student_id as StudentID,c.course_id as CourseID,c.coNum as coNum,p.ploNum as ploNum,100*sum(e.obtainedMarks)/sum(a.totalMarks) as marks
                       FROM spmapp_registration_t r,
                           spmapp_evaluation_t e,
                           spmapp_assessment_t a, 
                           spmapp_co_t c,
                           spmapp_plo_t p
                       WHERE r.registrationID = e.registration_id
                           and e.assessment_id = a.assessmentID
                           and a.co_id = c.coID
                           and c.plo_id = p.ploID
                            and c.course_id = '{}'
                       GROUP BY r.student_id,c.course_id,c.coID, p.ploID
                       )derived
                GROUP BY CourseID,coNum,ploNum
               '''.format(course))
        total = cursor.fetchone()[2]


    coplo = []
    temp = []
    for i in row:
        temp.append(i[2])
        print(temp)
        coplo.append([i[0], i[1]])
    temp = np.array(temp)

    success = np.round(temp / total * 100, 3)
    failCount = total - temp
    fail = np.round(failCount / total * 100, 3)
    row = np.column_stack((temp, success, failCount, fail)).tolist()

    finalRow = []
    for i in range(len(row)):
        tempRow = coplo[i]
        for j in range(len(row[i])):
            tempRow.append(row[i][j])
        finalRow.append(tempRow)

    return (finalRow, total)