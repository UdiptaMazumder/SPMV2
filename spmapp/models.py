from django.db import models

# Create your models here.

class School_T(models.Model):
    schoolID = models.CharField(max_length=5, primary_key=True)
    schoolName = models.CharField(max_length=50)

class Department_T(models.Model):
    departmentID = models.CharField(max_length=5, primary_key=True)
    departmentName = models.CharField(max_length=50)
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)