from django.db import connection

import numpy as np



import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django
django.setup()

from django.core.management import call_command

from spmapp.models import *

row = []

with connection.cursor() as cursor:
    cursor.execute('''
       SELECT sc.course_id,at.assessmentName,SUM(et.obtainedMarks)
       FROM spmapp_registration_t rt,
            spmapp_section_t sc,
            spmapp_assessment_t at,
            spmapp_evaluation_t et
            
            
        WHERE rt.student_id='{}'
        AND rt.semester='{}'
        AND rt.year='{}'
        AND rt.section_id=sc.sectionID
        AND rt.registrationID=et.registration_id
        AND at.section_id=rt.section_id
        
        
        
        GROUP BY rt.registrationID, at.assessmentName
        
        
        
    '''.format(1898336,"Spring",2020))

    row.append(cursor.fetchall())

for i in row:
    print(i)



