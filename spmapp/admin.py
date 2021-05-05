from django.contrib import admin
from .models import *


# Register your models here.


# admin.site.register(School_T)
# admin.site.register(Department_T)
# admin.site.register(Program_T)
# admin.site.register(Student_T)
# admin.site.register(VC_T)
# admin.site.register(Dean_T)
# admin.site.register(Head_T)
# admin.site.register(Faculty_T)
# admin.site.register(Course_T)
# admin.site.register(PrereqCourse_T)
# admin.site.register(Section_T)
# admin.site.register(PLO_T)
# admin.site.register(CO_T)
# admin.site.register(Registration_T)
# admin.site.register(Assessment_T)
# admin.site.register(Evaluation_T)

class School_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in School_T._meta.fields if field.name != "id"]


admin.site.register(School_T, School_TAdmin)


class Department_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Department_T._meta.fields if field.name != "id"]


admin.site.register(Department_T, Department_TAdmin)


class Program_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Program_T._meta.fields if field.name != "id"]


admin.site.register(Program_T, Program_TAdmin)


class Student_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Student_T._meta.fields if field.name != "id"]


admin.site.register(Student_T, Student_TAdmin)


class VC_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VC_T._meta.fields if field.name != "id"]


admin.site.register(VC_T, VC_TAdmin)


class Dean_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Dean_T._meta.fields if field.name != "id"]


admin.site.register(Dean_T, Dean_TAdmin)


class Head_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Head_T._meta.fields if field.name != "id"]


admin.site.register(Head_T, Head_TAdmin)


class Faculty_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Faculty_T._meta.fields if field.name != "id"]


admin.site.register(Faculty_T, Faculty_TAdmin)


class Course_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Course_T._meta.fields if field.name != "id"]


admin.site.register(Course_T, Course_TAdmin)

class PrereqCourse_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrereqCourse_T._meta.fields if field.name != "id"]


admin.site.register(PrereqCourse_T, PrereqCourse_TAdmin)


class Section_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Section_T._meta.fields if field.name != "id"]


admin.site.register(Section_T, Section_TAdmin)


class PLO_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PLO_T._meta.fields if field.name != "id"]


admin.site.register(PLO_T, PLO_TAdmin)


class CO_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CO_T._meta.fields if field.name != "id"]


admin.site.register(CO_T, CO_TAdmin)

class Registration_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Registration_T._meta.fields if field.name != "id"]


admin.site.register(Registration_T, Registration_TAdmin)


class Assessment_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Assessment_T._meta.fields if field.name != "id"]


admin.site.register(Assessment_T, Assessment_TAdmin)


class Evaluation_TAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Evaluation_T._meta.fields if field.name != "id"]


admin.site.register(Evaluation_T, Evaluation_TAdmin)



