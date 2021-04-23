from django.db import models

# Create your models here.

class School_T(models.Model):
    SchoolID = models.CharField(max_length=5, primary_key=True)
    SchoolName = models.CharField(max_length=50)

    def __str__(self):
        return self.SchoolName


class Department_T(models.Model):
    DepartmentID = models.CharField(max_length=5, primary_key=True)
    DepartmentName = models.CharField(max_length=50)
    SchoolID = models.ForeignKey(School_T, on_delete=models.CASCADE)


class Program_T(models.Model):
    ProgramID = models.AutoField(primary_key=True)
    ProgramName = models.CharField(max_length=70)
    DepartmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE, default='N/A')


class Student_T(models.Model):
    StudentID = models.CharField(max_length=7, primary_key=True)
    FirstName = models.CharField(max_length=50, null=True)
    LastName = models.CharField(max_length=50, null=True)
    DateOfBirth = models.DateField(null=True)
    Gender = models.CharField(max_length=6, null=True)
    Email = models.CharField(max_length=50, null=True)
    Phone = models.CharField(max_length=15, null=True)
    Address = models.CharField(max_length=50, null=True)
    EnrollmentDate = models.DateField(null=True)
    ProgramID = models.ForeignKey(Program_T, on_delete=models.CASCADE, default='N/A')
    DepartmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class Employee_T(models.Model):
    FirstName = models.CharField(max_length=30, null=True)
    LastName = models.CharField(max_length=30, null=True)
    DateOfBirth = models.DateField(null=True)
    Gender = models.CharField(max_length=6, null=True)
    Email = models.CharField(max_length=30, null=True)
    Phone = models.CharField(max_length=15, null=True)
    Address = models.CharField(max_length=30, null=True)
    EmployeeType = models.CharField(max_length=1, null=True)

    class Meta:
        abstract = True



class VC_T(Employee_T):
    VCID = models.CharField(max_length=4, primary_key=True)
    StartDate = models.DateField()
    EndDate = models.DateField(null=True)


class Dean_T(Employee_T):
    DeanID = models.CharField(max_length=4, primary_key=True)
    StartDate = models.DateField()
    EndDate = models.DateField(null=True)
    SchoolID = models.ForeignKey(School_T, on_delete=models.CASCADE)


class Head_T(Employee_T):
    HeadID = models.CharField(max_length=4, primary_key=True)
    StartDate = models.DateField()
    EndDate = models.DateField(null=True)
    DepartmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class Faculty_T(Employee_T):
    FacultyID = models.CharField(max_length=4, primary_key=True)
    StartDate = models.DateField(null=True)
    Rank = models.CharField(max_length=50, null=True)
    DepartmentID = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class Course_T(models.Model):
    CourseID = models.CharField(max_length=7, primary_key=True)
    CourseName = models.CharField(max_length=50, null=True)
    NumOfCredits = models.DecimalField(max_digits=2, decimal_places=1)
    ProgramID = models.ForeignKey(Program_T, on_delete=models.CASCADE)

    def __str__(self):
        return self.CourseID


class PrereqCourse_T(models.Model):
    CourseID = models.ForeignKey(Course_T, on_delete=models.CASCADE, related_name='Course')
    PreReqCourseID = models.ForeignKey(Course_T, on_delete=models.CASCADE, related_name='PreRequisite')


class PLO_T(models.Model):
    PLOID = models.AutoField(primary_key=True)
    PLONum = models.IntegerField()
    ProgramID = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    Details = models.CharField(max_length=50)



class Section_T(models.Model):
    ScetionID = models.AutoField(primary_key=True)
    SectionNum = models.IntegerField()
    CourseID = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    FacultyID = models.ForeignKey(Faculty_T, on_delete=models.CASCADE)
    Semester = models.CharField(max_length=6)
    Year = models.CharField(max_length=4)


class Registration_T(models.Model):
    RegistrationID = models.AutoField(primary_key=True)
    StudentID = models.ForeignKey(Student_T, on_delete=models.CASCADE)
    SectionID = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    Semester = models.CharField(max_length=6)
    Year = models.CharField(max_length=4)


class CO_T(models.Model):
    COID = models.AutoField(primary_key=True, default='N/A')
    CONum = models.IntegerField()
    PLOID = models.ForeignKey(PLO_T, on_delete=models.CASCADE, default='N/A')
    CourseID = models.ForeignKey(Course_T, on_delete=models.CASCADE, default='N/A')
    Thresold = models.FloatField(default=40)


class Assessment_T(models.Model):
    AssessmentID = models.AutoField(primary_key=True)
    AssessmentName = models.CharField(max_length=30)
    QuestionNum = models.IntegerField()
    TotalMarks = models.FloatField()
    COID = models.ForeignKey(CO_T, on_delete=models.CASCADE)
    SectionID = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    Weight = models.FloatField()


class Evaluation_T(models.Model):
    EvaluationID = models.AutoField(primary_key=True)
    ObtainedMarks = models.FloatField()
    AssessmentID = models.ForeignKey(Assessment_T, on_delete=models.CASCADE)
    RegistrationID = models.ForeignKey(Registration_T, on_delete=models.CASCADE)



