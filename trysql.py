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
        Select r.registrationID
        
        from spmapp_registration_t r
        
        where r.student_id='{}'
        
        
    '''.format(1416455))

    row.append(cursor.fetchall())

for i in row:
    print(i)



