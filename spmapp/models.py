from django.db import models

# Create your models here.

class School_T(models.Model):
    schoolID = models.CharField(max_length=5, primary_key=True)
    schoolName = models.CharField(max_length=50)

    def __str__(self):
        return self.schoolID


class Department_T(models.Model):
    departmentID = models.CharField(max_length=5, primary_key=True)
    departmentName = models.CharField(max_length=50)
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)

    def __str__(self):
        return self.departmentID


class Program_T(models.Model):
    programID = models.AutoField(primary_key=True)
    programName = models.CharField(max_length=70)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE, default='N/A')

    def __str__(self):
        return self.programName




class Student_T(models.Model):
    studentID = models.CharField(max_length=7, primary_key=True)
    firstName = models.CharField(max_length=50, null=True)
    lastName = models.CharField(max_length=50, null=True)
    dateOfBirth = models.DateField(null=True)
    gender = models.CharField(max_length=6, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=50, null=True)
    enrollmentDate = models.DateField(null=True)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE, default='N/A')
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)

    def __str__(self):
        return self.studentID


class Employee_T(models.Model):
    firstName = models.CharField(max_length=30, null=True)
    lastName = models.CharField(max_length=30, null=True)
    dateOfBirth = models.DateField(null=True)
    gender = models.CharField(max_length=6, null=True)
    email = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=30, null=True)
    employeeType = models.CharField(max_length=1, null=True)

    class Meta:
        abstract = True


class VC_T(Employee_T):
    vcID = models.CharField(max_length=4, primary_key=True)
    startDate = models.CharField(max_length=15, default='N/A')
    endDate = models.CharField(max_length=15, default='N/A')


class Dean_T(Employee_T):
    deanID = models.CharField(max_length=4, primary_key=True)
    startDate = models.CharField(max_length=15, default='N/A')
    endDate = models.CharField(max_length=15, default='N/A')
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)


class Head_T(Employee_T):
    headID = models.CharField(max_length=4, primary_key=True)
    startDate = models.CharField(max_length=15,default='N/A')
    endDate = models.CharField(max_length=15,default='N/A')
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class Faculty_T(Employee_T):
    facultyID = models.IntegerField(primary_key=True)
    startDate = models.DateField(null=True)
    rank = models.CharField(max_length=50, null=True)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstName + " "+ self.lastName


class Course_T(models.Model):
    courseID = models.CharField(max_length=7, primary_key=True)
    courseName = models.CharField(max_length=50, null=True)
    numOfCredits = models.DecimalField(max_digits=2, decimal_places=1)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    courseType = models.CharField(max_length=15)

    def __str__(self):
        return self.courseID


class PrereqCourse_T(models.Model):
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE, related_name='Course')
    preReqCourse = models.ForeignKey(Course_T, on_delete=models.CASCADE, related_name='PreRequisite')


class PLO_T(models.Model):
    ploID = models.AutoField(primary_key=True)
    ploNum = models.CharField(max_length=5)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    details = models.CharField(max_length=50)

    def __str__(self):
        return self.ploNum


class Section_T(models.Model):
    sectionID = models.AutoField(primary_key=True)
    sectionNum = models.IntegerField()
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty_T, on_delete=models.CASCADE)
    semester = models.CharField(max_length=15)


    def __str__(self):
        return str(self.sectionNum)


class Registration_T(models.Model):
    registrationID = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    semester = models.CharField(max_length=15)
    year = models.IntegerField(default=2020,null=True)

    def __str__(self):
        return str(self.registrationID)



class CO_T(models.Model):
    coID = models.AutoField(primary_key=True)
    coNum = models.CharField(max_length=4)
    plo = models.ForeignKey(PLO_T, on_delete=models.CASCADE, default='N/A')
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE, default='N/A')
    thresold = models.FloatField(default=40)

    def __str__(self):
        return self.coNum


class Assessment_T(models.Model):
    assessmentID = models.AutoField(primary_key=True)
    assessmentName = models.CharField(max_length=30)
    questionNum = models.IntegerField()
    totalMarks = models.FloatField()
    co = models.ForeignKey(CO_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    weight = models.FloatField()

    def __str__(self):
        return self.assessmentName + " "+str(self.questionNum)



class Evaluation_T(models.Model):
    evaluationID = models.AutoField(primary_key=True)
    obtainedMarks = models.FloatField()
    assessment = models.ForeignKey(Assessment_T, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration_T, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.evaluationID)

