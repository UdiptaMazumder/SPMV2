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



def getCourseWisePLO(studentID,cat):
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
                if cat == "report":
                    temptable.append('N/A')
                elif cat == "chart":
                    temptable.append(0)
        table.append(temptable)
    return plo, courses, table





