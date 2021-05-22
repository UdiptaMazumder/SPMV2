from django.db import connection

import numpy as np

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from django.core.management import call_command

from spmapp.models import *


def getStudentWisePLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT p.ploNum as ploNum,100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as PLOper
            FROM spmapp_registration_t r,
                spmapp_assessment_t a, 
                spmapp_evaluation_t e,
                spmapp_co_t co, 
                spmapp_plo_t p
            WHERE r.registrationID = e.registration_id 
                and e.assessment_id = a.assessmentID
                and a.co_id=co.coID 
                and co.plo_id = p.ploID
                and r.student_id = '{}' 
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
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6", "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in courses:
        temptable = []

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    temptable.append(np.round(k[2], 2))
                    found = True
            if not found:
                temptable.append(0)
        table.append(temptable)
    return (plo, courses, table)


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
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6", "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in cos:
        temptable = []

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    temptable.append(np.round(k[2], 2))
                    found = True
            if not found:
                temptable.append(0)
        table.append(temptable)
    return (plo, cos, table)


def getPLOwithDeptAvg(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT p.ploNum as ploNum,100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as PLOper,derived.DeptAvg
            FROM 
                spmapp_registration_t r,
                spmapp_student_t st,
                spmapp_assessment_t a, 
                spmapp_evaluation_t e,
                spmapp_co_t co, 
                spmapp_plo_t p,
                (
                    SELECT d.departmentID as Dept,p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as DeptAvg
                    
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
                    GROUP BY p.ploID
                        
                ) derived
            WHERE r.registrationID = e.registration_id 
                and r.student_id = st.studentID
                and e.assessment_id = a.assessmentID
                and a.co_id=co.coID 
                and co.plo_id = p.ploID
                and r.student_id = '{}' 
                and st.department_id = derived.Dept
                and p.ploNum = derived.ploNum
            GROUP BY  p.ploID
            '''.format(studentID))
        row = cursor.fetchall()
        print(row)


def getDeptWisePLO(dept):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as DeptAvg
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
                GROUP BY p.ploID
               '''.format(dept))
        row = cursor.fetchall()
    print(row)


def getDeptWiseEnrolledStudents(semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT d.departmentID, count( distinct st.studentID)
            FROM spmapp_department_t d,
                spmapp_student_t st,
                spmapp_registration_t r
            WHERE r.student_id = st.studentID
                and st.department_id = d.departmentID
                and r.semester = '{}'
                and r.year = '{}'
            GROUP BY d.departmentID
            '''.format(semester, year))
        row = cursor.fetchall()

    return row


def getSchoolWiseEnrolledStudents(semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT s.schoolID, count( distinct st.studentID)
            FROM spmapp_school_t s,
                spmapp_department_t d,
                spmapp_student_t st,
                spmapp_registration_t r
            WHERE r.student_id = st.studentID
                and st.department_id = d.departmentID
                and d.school_id = s.schoolID
                and r.semester = '{}'
                and r.year = '{}'
            GROUP BY s.schoolID
            '''.format(semester, year))
        row = cursor.fetchall()

    return row


def getProgramWiseEnrolledStudents(semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT p.programName, count( distinct st.studentID)
            FROM spmapp_program_t p,
                spmapp_student_t st,
                spmapp_registration_t r
            WHERE r.student_id = st.studentID
                and st.program_id = p.programID
                and r.semester = '{}'
                and r.year = '{}'
            GROUP BY p.programID
            '''.format(semester, year))
        row = cursor.fetchall()

    return row


def getAllSemesters():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT semester, year
            FROM spmapp_registration_t r

        ''')

        row = cursor.fetchall()
    return row


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

    print(studentlist)


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


def getProgramWisePLO(program):
    plo = ['PLO1', 'PLO2', 'PLO3', 'PLO4', 'PLO5', 'PLO6', 'PLO7', 'PLO8', 'PLO9', 'PLO10', 'PLO11', 'PLO12']
    achieved = []
    attempted = []

    for p in plo:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT COUNT (actual)
                FROM(
                    SELECT AVG(percourse) as actual
                    FROM (
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
                        GROUP BY r.student_id,c.coID) per
                    GROUP BY per.StudentID) avgTable
          '''.format(program))
            row = cursor.fetchall()

            if row is not None:
                attempted.append(row)
            else:
                attempted.append(0)

    for p in plo:
        with connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT(*)
                FROM(
                    SELECT StudentID, AVG(percourse) as actual
                    FROM (
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
                        GROUP BY r.student_id,r.registrationID) per
                    GROUP BY per.StudentID) avgTable
                WHERE actual>=40

          '''.format(program))
            row = cursor.fetchall()

            if row is not None:
                achieved.append(row)
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

        print(row)

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

        print(total)

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


def getStudentWisePLO2(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum as plonum,100*(sum( e.obtainedMarks)/sum( a.totalMarks)) as plopercent
                FROM spmapp_registration_t r,
                    spmapp_assessment_t a, 
                    spmapp_evaluation_t e,
                    spmapp_co_t co, 
                    spmapp_plo_t p
                WHERE  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and  r.student_id = '{}'
                GROUP BY  p.ploID

                '''.format(studentID))
        row = cursor.fetchall()
    return row

print(getStudentWisePLO2(1416455))