import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *


reglist = Registration_T.objects.all()

for r in reglist:
    if(len(r.semester)==6):
        st = r.semester+" "+str(r.year)
        r.semester=st
        r.save()

sectionlist = Section_T.objects.all()

for s in sectionlist:
    if(len(s.semester)==6):
        st = s.semester+" "+str(s.year)
        s.semester = st
        s.save()
