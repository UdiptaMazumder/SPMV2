import pandas as pd
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

asslist = Assessment_T.objects.all()

for i in range(100,1288):
    ass = asslist[i-1]
    if i%11==9:
        ass.co_id+=1
    elif i%11==10:
        ass.co_id+=1
    if i%11==0:
        ass.co_id+=2
    ass.save()

