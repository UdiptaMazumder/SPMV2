import pandas as pd
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

colist = CO_T.objects.all()

for i in colist:
    if i.course_id in ('CSE201', 'CSE104'):
        i.plo_id += 4
        i.save()
    elif i.course_id in ('CSE203', 'CSE204'):
        i.plo_id += 8
        i.save()
