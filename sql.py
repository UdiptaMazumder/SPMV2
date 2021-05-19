from django.db import connection

import numpy as np

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from django.core.management import call_command

from spmapp.models import *


def getStudentWiseOverallPLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum,100*(sum( e.obtainedMarks)/sum( a.totalMarks)) as ploper
                FROM spmapp_registration_t r,
                    spmapp_assessment_t a, 
                    spmapp_evaluation_t e,
                    spmapp_co_t co, spmapp_plo_t p
                WHERE r.student_id = '{}' 
                    and  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID and co.plo_id = p.ploID
                GROUP BY  p.ploID

                '''.format(studentID))
        row = cursor.fetchall()

    return row


def getStudentWisePLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            Select  p.ploNum as PloNum, sum(e.obtainedMarks)/Total,co.course_id
            FROM spmapp_registration_t r,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t co,
                spmapp_plo_t p,
                (SELECT  p.ploNum as PloNum, sum(a.totalMarks) AS Total,r.registrationID
                FROM spmapp_registration_t r,
                    spmapp_evaluation_t e,
                    spmapp_assessment_t a,
                    spmapp_co_t co,
                    spmapp_plo_t p
                WHERE e.registration_id = r.registrationID
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and r.student_id = '{}' 
                GROUP BY p.ploID) derived
                
            WHERE e.registration_id = derived.registrationID
                and e.assessment_id = a.assessmentID
                and a.co_id=co.coID 
                and co.plo_id = p.ploID
                and p.ploNum = derived.PloNum
            GROUP BY p.ploID,co.course_id
                    
            

            '''.format(studentID))
        row = cursor.fetchall()

    return row


def getCourseWisePLO(studentID, cat):
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
    for k in row:
        print(k)

    table = []
    courses = []

    for entry in row:
        if entry[1] not in courses:
            courses.append(entry[1])
    courses.sort()
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
                if cat == "report":
                    temptable.append('N/A')
                elif cat == "chart":
                    temptable.append(0)
        table.append(temptable)
    return plo, courses, table


def getStudentWiseGPA(studentID, semester, year):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT sum(Credits*grade)/sum(Credits)
            FROM(   
                SELECT  Credits,
                    CASE
                        WHEN sum(Marks) >= 85 THEN 4.0
                        WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                        WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                        WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                        WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                        WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                        WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                        WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                        WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                        WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                        ELSE 0.0
                    END as grade
                FROM(
                    SELECT c.courseID as CourseID,a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                    FROM spmapp_registration_t r,
                        spmapp_section_t sc, 
                        spmapp_course_t c,
                        spmapp_assessment_t a, 
                        spmapp_evaluation_t e
                    WHERE r.student_id = '{}' 
                        and r.semester='{}' 
                        and r.year ='{}' 
                        and r.section_id = sc.sectionID
                        and sc.course_id = c.courseID 
                        and r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID
                    GROUP BY  c.courseID,a.assessmentName) Derived 
                GROUP BY CourseID) Derived
                    '''.format(studentID, semester, year))

        row = cursor.fetchall()[0][0]
    return np.round(row, 3)


def getSchoolWiseGPA(school, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT AVG(grade) as avgGrade
               FROM(
                   SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                   FROM(   
                       SELECT  StudentID,Credits,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                                spmapp_department_t d,
                                spmapp_school_t s,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = d.departmentID
                                and d.school_id = s.schoolID
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.courseID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and s.schoolID = '{}'
                                and r.semester='{}'
                                and r.year ='{}' 
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(school, semester, year))

        row = cursor.fetchall()[0][0]
    return np.round(row, 3)


def getDeptWiseGPA(dept, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT AVG(grade) as avgGrade
            FROM(
                SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                FROM(   
                    SELECT  StudentID,Credits,
                        CASE
                            WHEN sum(Marks) >= 85 THEN 4.0
                            WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                            WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                            WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                            WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                            WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                            WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                            WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                            WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                            WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                            ELSE 0.0
                        END as gradepoint
                    FROM(
                        SELECT st.studentID as StudentID,c.courseID as CourseID,
                            a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                        FROM spmapp_student_t st,
                            spmapp_registration_t r,
                            spmapp_section_t sc, 
                            spmapp_course_t c,
                            spmapp_assessment_t a, 
                            spmapp_evaluation_t e
                        WHERE st.studentID = r.student_id
                            and r.section_id = sc.sectionID
                            and sc.course_id = c.courseID 
                            and r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and st.department_id = '{}'
                            and r.semester='{}'
                            and r.year ='{}' 
                        GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                    GROUP BY StudentID,CourseID) Derived2
                GROUP BY StudentID)
                    '''.format(dept, semester, year))

        row = cursor.fetchall()[0][0]
    return np.round(row, 3)


def getProgramWiseGPA(program, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT AVG(grade) as avgGrade
               FROM(
                   SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                   FROM(   
                       SELECT  StudentID,Credits,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and sc.course_id = c.courseID 
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and st.program_id = '{}'
                               and r.semester='{}'
                               and r.year ='{}' 
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(program, semester, year))

        row = cursor.fetchall()[0][0]
    return np.round(row, 3)


def getCourseWiseGPA(course, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  StudentID,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks
                           FROM spmapp_student_t st,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and sc.course_id = c.courseID 
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and c.courseID = '{}'
                               and r.semester='{}'
                               and r.year ='{}' 
                           GROUP BY  st.studentID,a.assessmentName) Derived
                       GROUP BY StudentID) Derived2
                       '''.format(course, semester, year))

        row = cursor.fetchall()[0][0]
    return np.round(row, 3)


def getInstructorWiseGPA(instructor, semester, year):
    with connection.cursor() as cursor:
        cursor.execute('''
               SELECT AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT  StudentID,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks
                           FROM spmapp_student_t st,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and sc.faculty_id = '{}'
                               and r.semester='{}'
                               and r.year ='{}' 
                           GROUP BY  st.studentID,a.assessmentName) Derived
                       GROUP BY StudentID) Derived2
                       '''.format(instructor, semester, year))

        row = cursor.fetchall()[0][0]
    return np.round(row, 3)


def getAllSemesters():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT semester
            FROM spmapp_registration_t r

        ''')

        row = cursor.fetchall()
    return row


def getInstructorWiseGPAForCourse(course, semesters):
    cursor = connection.cursor()

    if len(semesters) == 1:
        print(semesters[0])
        cursor.execute('''
               SELECT Semester,FacultyID, AVG(gradepoint) as avgGrade
               FROM(   
                       SELECT Semester, FacultyID,StudentID,
                           CASE
                               WHEN sum(Marks) >= 85 THEN 4.0
                               WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                               WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                               WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                               WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                               WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                               WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                               WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                               WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                               WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                               ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT r.semester as Semester, sc.faculty_id as FacultyID, st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks
                           FROM spmapp_student_t st,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                               and r.section_id = sc.sectionID
                               and r.registrationID = e.registration_id 
                               and e.assessment_id = a.assessmentID
                               and sc.course_id = '{}'
                               and r.semester = '{}'
                           GROUP BY  r.semester, sc.faculty_id,st.studentID,a.assessmentName) Derived
                       GROUP BY Semester,FacultyID,StudentID) Derived2
               GROUP BY Semester,FacultyID
                       '''.format(course, semesters[0]))
    else:
        cursor.execute('''
                      SELECT Semester,FacultyID, AVG(gradepoint) as avgGrade
                      FROM(   
                              SELECT Semester, FacultyID,StudentID,
                                  CASE
                                      WHEN sum(Marks) >= 85 THEN 4.0
                                      WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                      WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                      WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                      WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                      WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                      WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                      WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                      WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                      WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                      ELSE 0.0
                                  END as gradepoint
                              FROM(
                                  SELECT r.semester as Semester, sc.faculty_id as FacultyID, st.studentID as StudentID,c.courseID as CourseID,
                                      a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks
                                  FROM spmapp_student_t st,
                                      spmapp_registration_t r,
                                      spmapp_section_t sc, 
                                      spmapp_course_t c,
                                      spmapp_assessment_t a, 
                                      spmapp_evaluation_t e
                                  WHERE st.studentID = r.student_id
                                      and r.section_id = sc.sectionID
                                      and r.registrationID = e.registration_id 
                                      and e.assessment_id = a.assessmentID
                                      and sc.course_id = '{}'
                                      and r.semester in {}
                                  GROUP BY  r.semester, sc.faculty_id,st.studentID,a.assessmentName) Derived
                              GROUP BY Semester,FacultyID,StudentID) Derived2
                      GROUP BY Semester,FacultyID
                      '''.format(course, str(tuple(semesters))))
    row = cursor.fetchall()

    return row


def trynew():
    cursor = connection.cursor()
    cs = ['CSE104', 'CSE201']

    cursor.execute('''
                    SELECT * 
                    FROM spmapp_course_t
                    where courseID in {}
    '''.format(str(tuple(cs))))

    row = cursor.fetchall()

    print(row)


def getheadwiseGPA(head):
    semlist = getAllSemesters()

    b = -1
    e = -1

    for s in range(0, len(semlist)):
        if semlist[s][0] == head.startDate:
            b = s

        if head.endDate == 'N/A':
            e = len(semlist) - 1
        elif semlist[s][0] == head.endDate:
            e = s

    semesters = []

    for i in range(b, e + 1):
        semesters.append(semlist[i][0])

    cursor = connection.cursor()

    if len(semesters) == 1:
        cursor.execute('''
                SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                                spmapp_department_t d,
                                spmapp_head_t h,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = h.department_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.courseID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and h.headID = '{}'
                                and r.semester='{}'
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(head.headID, semesters[0]))
    else:
        cursor.execute('''
                      SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                                spmapp_department_t d,
                                spmapp_head_t h,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = h.department_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.courseID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and h.headID = '{}'
                                and r.semester in {}
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(head.headID, str(tuple(semesters))))
    row = cursor.fetchall()[0][0]

    return row


def getDeanWiseGPA(dean):
    semlist = getAllSemesters()

    b = -1
    e = -1

    for s in range(0, len(semlist)):
        if semlist[s][0] == dean.startDate:
            b = s
        if dean.endDate == 'N/A':
            e = len(semlist) - 1
        elif semlist[s][0] == dean.endDate:
            e = s
    semesters = []

    for i in range(b, e + 1):
        semesters.append(semlist[i][0])

    cursor = connection.cursor()

    if len(semesters) == 1:
        cursor.execute('''
                SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                                spmapp_department_t d,
                                spmapp_dean_t dn,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = d.departmentID
                                and d.school_id = dn.school_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.courseID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and dn.deanID= '{}'
                                and r.semester='{}'
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(dean.deanID, semesters[0]))
    else:
        cursor.execute('''
                       SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                                spmapp_department_t d,
                                spmapp_dean_t dn,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and st.department_id = d.departmentID
                                and d.school_id = dn.school_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.courseID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and dn.deanID= '{}'
                                and r.semester in {}
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(dean.deanID, str(tuple(semesters))))
    row = cursor.fetchall()[0][0]

    return row


def getVCWiseGPA(vc):
    semlist = getAllSemesters()

    b = -1
    e = -1

    for s in range(0, len(semlist)):
        if semlist[s][0] == vc.startDate:
            b = s
        if vc.endDate == 'N/A':
            e = len(semlist) - 1
        elif semlist[s][0] == vc.endDate:
            e = s
    semesters = []

    for i in range(b, e + 1):
        semesters.append(semlist[i][0])

    cursor = connection.cursor()

    if len(semesters) == 1:
        cursor.execute('''
                SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                                spmapp_department_t d,
                                spmapp_dean_t dn,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.courseID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and r.semester='{}'
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(semesters[0]))
    else:
        print(semesters)
        print(b,e)
        cursor.execute('''
                       SELECT AVG(grade) as avgGrade
                FROM(
                    SELECT StudentID,sum(Credits*gradepoint)/sum(Credits) as grade
                    FROM(   
                        SELECT  StudentID,Credits,
                            CASE
                                   WHEN sum(Marks) >= 85 THEN 4.0
                                   WHEN sum(Marks) >= 80 AND sum(Marks)<85 THEN 3.7
                                   WHEN sum(Marks) >= 75 AND sum(Marks)<80 THEN 3.3
                                   WHEN sum(Marks) >= 70 AND sum(Marks)<75 THEN 3.0
                                   WHEN sum(Marks) >= 65 AND sum(Marks)<70 THEN 2.7
                                   WHEN sum(Marks) >= 60 AND sum(Marks)<65 THEN 2.3
                                   WHEN sum(Marks) >= 55 AND sum(Marks)<60 THEN 2.0
                                   WHEN sum(Marks) >= 50 AND sum(Marks)<55 THEN 1.7
                                   WHEN sum(Marks) >= 45 AND sum(Marks)<50 THEN 1.3
                                   WHEN sum(Marks) >= 40 AND sum(Marks)<45 THEN 1.0
                                   ELSE 0.0
                           END as gradepoint
                       FROM(
                           SELECT st.studentID as StudentID,c.courseID as CourseID,
                               a.weight*(sum(e.obtainedMarks)/sum(a.totalMarks)) as Marks, c.numOfCredits as Credits
                           FROM spmapp_student_t st,
                                spmapp_department_t d,
                                spmapp_dean_t dn,
                               spmapp_registration_t r,
                               spmapp_section_t sc, 
                               spmapp_course_t c,
                               spmapp_assessment_t a, 
                               spmapp_evaluation_t e
                           WHERE st.studentID = r.student_id
                                and r.section_id = sc.sectionID
                                and sc.course_id = c.courseID 
                                and r.registrationID = e.registration_id 
                                and e.assessment_id = a.assessmentID
                                and r.semester in {}
                           GROUP BY  st.studentID,c.courseID,a.assessmentName) Derived1
                       GROUP BY StudentID,CourseID) Derived2
                   GROUP BY StudentID)
                       '''.format(str(tuple(semesters))))
    row = cursor.fetchall()[0][0]

    return row

