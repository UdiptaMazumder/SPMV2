import pandas as pd

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SPMV2.settings")

import django

django.setup()

from spmapp.models import *


vfnames = ["M. Omar","Tanweer"]

vlnames = ["Rahman", "Hasan"]

