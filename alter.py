import pandas as pd
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *

#rlist = Registration_T.objects.all()

#for i in rlist:
 #   st = i.semester + " " + str(i.year)
  ## i.save()

