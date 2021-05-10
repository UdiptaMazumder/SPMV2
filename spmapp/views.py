import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .queries import *
from spmapp.models import *


# Create your views here.

#list

schoollist = School_T.objects.all()
deptlist = Department_T.objects.all()
programlist = Program_T.objects.all()
courselist = Course_T.objects.all()

def loginview(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def logoutview(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url="/login/")
def homeview(request):
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

        if group == 'Student':
            return shome(request)
        if group == 'Faculty':
            return fhome(request)
        if group == 'Higher Authority':
            return hahome(request)
        else:
            return redirect('/')





@login_required(login_url="/login/")
def shome(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    studentid = 1416455
    st = Student_T.objects.get(pk=1416455)
    dept = st.department_id

    row = getStudentWiseOverallPLO(studentid)
    chart1 = 'PLO Achievement'
    plolabel1 = []
    plodata1 = []

    for i in row:
        plolabel1.append(i[0])
        plodata1.append(i[1])

    row = getDeptWisePLO(dept)
    chart2 = 'PLO Achievement with Department Average'
    plolabel2 = []
    plodata2 = []

    for i in row:
        plolabel2.append(i[0])
        plodata2.append(i[1])

    semesters = getAllSemesters()
    chart3 = "Student Wise Gpa"
    gpalabel1 = []
    gpadata1 = []
    row = []

    for s in semesters:
        row.append((s[0] + "'" + str(s[1]), getStudentWiseGPA(studentid, s[0], s[1])))

    for i in row:
        gpalabel1.append(i[0])
        gpadata1.append(i[1])

    chart4 = "Department Wise Gpa"
    gpalabel2 = []
    gpadata2 = []
    row = []

    row.append(("Spring" + "'" + str(2020), getDeptWiseGPA('ACN', "Spring", 2020)))
    row.append(("Summer" + "'" + str(2020), getDeptWiseGPA('ACN', "Summer", 2020)))
    row.append(("Autumn" + "'" + str(2020), getDeptWiseGPA('ACN', "Autumn", 2020)))

    for i in row:
        gpalabel2.append(i[0])
        gpadata2.append(i[1])

    return render(request, 'student/studenthome.html', {
        'name': name,
        'usertype': type,

        'chart1': chart1,
        'plolabel1': plolabel1,
        'plodata1': plodata1,

        'chart2': chart2,
        'plolabel2': plolabel2,
        'plodata2': plodata2,

        'chart3': chart3,
        'gpalabel1': gpalabel1,
        'gpadata1': gpadata1,

        'chart4': chart4,
        'gpalabel2': gpalabel2,
        'gpadata2': gpadata2,

    })


def cowiseplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    studentid = 1416455
    st = Student_T.objects.get(pk=1416455)
    dept = st.department_id

    (plo, co, table) = getCOWisePLO(studentid, 'chart')

    return render(request, 'student/cowise.html', {
        'name': name,
        'usertype': type,
        'plo': plo,
        'co': co,
        'table': table

    })


def coursewiseplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    studentid = 1416455
    st = Student_T.objects.get(pk=1416455)
    dept = st.department_id

    (plo, courses, table) = getCourseWisePLO(studentid, 'chart')

    return render(request, 'student/coursewise.html', {
        'name': name,
        'usertype': type,
        'plo': plo,
        'courses': courses,
        'table': table,

    })


def plotable(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    studentid = 1416455
    st = Student_T.objects.get(pk=1416455)
    dept = st.department_id

    (plo, courses, table) = getCourseWisePLO(studentid, 'report')
    range = len(courses)
    print(range)

    return render(request, 'student/plotable.html', {
        'name': name,
        'usertype': type,
        'plo': plo,
        'courses': courses,
        'table': table,
        'range': range,

    })


@login_required(login_url="/login/")
def fhome(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    deptT = Faculty_T.objects.get(pk=int(request.user.username))

    dept = deptT.department_id

    print(dept)

    row = getDeptWisePLO(dept)
    chart2 = 'PLO Achievement with Department Average'
    plolabel = []
    plodata = []

    for i in row:
        plolabel.append(i[0])
        plodata.append(i[1])

    gpalabel = []
    gpadata = []

    semesters = getAllSemesters()

    for s in semesters:
        gpadata.append(getDeptWiseGPA(dept, s[0], s[1]))
        gpalabel.append(s[0]+' '+str(s[1]))

    return render(request,'facultyhome.html',{
        'name':name,
        'usertype':type,

        'plolabel':plolabel,
        'plodata':plodata,
        'gpalabel':gpalabel,
        'gpadata': gpadata,

    })








def userprofile(request):
    return render(request, 'page-user.html', {})


# higher authority

@login_required(login_url="/login/")
def hahome(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name


    totalStudents = len(studentlist)

    schools = []

    for s in schoollist:
        schools.append(s.schoolID)

    semesters = getAllSemesters()

    # schoolwise gpa
    sgpatable = []
    sgpalabel = []

    for s in semesters:
        sgpalabel.append(s[0] + " " + str(s[1]))

    for school in schools:

        gpa = []
        temp = []

        for s in semesters:
            temp.append(getSchoolWiseGPA(school, s[0], s[1]))

        for i in temp:
            gpa.append(i)
        sgpatable.append(gpa)

    # deptwise gpa

    depts = []

    for d in deptlist:
        depts.append(d.departmentID)

    # schoolwise gpa
    dgpatable = []
    dgpalabel = []

    for s in semesters:
        dgpalabel.append(s[0] + " " + str(s[1]))

    for dept in depts:
        gpa = []
        temp = []

        for s in semesters:
            temp.append(getDeptWiseGPA(dept, s[0], s[1]))

        for i in temp:
            gpa.append(i)
        dgpatable.append(gpa)

    # programwise gpa
    programs = []
    programnames = []

    for p in programlist:
        programs.append(p.programID)
        programnames.append(p.programName)

    pgpatable = []
    pgpalabel = []

    for s in semesters:
        pgpalabel.append(s[0] + " " + str(s[1]))

    for p in programs:
        gpa = []
        for s in semesters:
            gpa.append(getProgramWiseGPA(p, s[0], s[1]))
        pgpatable.append(gpa)

    return render(request, 'hahome.html', {
        'name': name,
        'usertype': type,

        'schools': schools,
        'sgpatable': sgpatable,
        'sgpalabel': sgpalabel,

        'depts': depts,
        'dgpatable': dgpatable,
        'dgpalabel': sgpalabel,

        'programs': programnames,
        'pgpatable': pgpatable,
        'pgpalabel': pgpalabel,
        'totalstudents':totalStudents,

    })


def plo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        studentid = request.POST.get('student-id')

        row = getStudentWiseOverallPLO(studentid)
        plo1 = []
        table1 = []

        for i in row:
            plo1.append(i[0])
            table1.append(i[1])

        (plo2, co, table2) = getCOWisePLO(studentid, 'chart')
        (plo3, courses, table3) = getCourseWisePLO(studentid, 'chart')

        response = {
            'name': name,
            'usertype': type,

            'plo1': plo1,
            'table1': table1,

            'plo2': plo2,
            'table2': table2,
            'co': co,

            'plo3': plo3,
            'table3': table3,
            'courses': courses,
        }

        return render(request, 'plo.html', response)
    else:
        return render(request, 'plo.html', {
            'name': name,
            'usertype': type
        })


def enrollment(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        year = request.POST['year']

        year = int(year)

        semesters = getAllSemesters()

        schools = []

        # schoolwise students

        for s in schoollist:
            schools.append(s.schoolID)

        snum = []
        for school in schools:
            num = 0

            for s in semesters:
                if (int(s[1]) == year):
                    num += getSchoolWiseEnrolledStudents(school, s[0], s[1])
            snum.append(num)

        # deptwise students

        depts = []

        for d in deptlist:
            depts.append(d.departmentID)

        dnum = []

        for dept in depts:
            num = 0

            for s in semesters:
                if (s[1] == year):
                    num += getDeptWiseEnrolledStudents(dept, s[0], s[1])
            dnum.append(num)

        # programwise gpa
        programs = []
        programnames = []

        for p in programlist:
            programs.append(p.programID)
            programnames.append(p.programName)

        pnum = []

        for p in programs:
            num = 0

            for s in semesters:
                if (s[1] == year):
                    num += getProgramWiseEnrolledStudents(p, s[0], s[1])
            pnum.append(num)

        return render(request, 'enrollment.html', {
            'name': name,
            'usertype': type,

            'school': schools,
            'snum': snum,
            'depts': depts,
            'dnum': dnum,
            'program': programnames,
            'pnum': pnum
        })
    else:
        return render(request, 'enrollment.html', {
            'name': name,
            'usertype': type
        })


def studentplotable(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        studentid = request.POST.get('student-id')
        (plo, courses, table) = getCourseWisePLO(studentid, 'report')
        range = len(courses)
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'plo': plo,
            'courses': courses,
            'table': table,
            'range': range,

        })
    else:
        return render(request, 'studentplotable.html',{
            'name':name,
            'usertype':type,
        })


def plostats(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    programs = []

    for p in programlist:
        programs.append(p.programName)

    if request.method == 'POST':
        prog = request.POST['program']

        print(prog)

        program = 1

        for p in programlist:
            print(p.programName)
            if p.programName == prog:
                program1 = p.programID

        (plo, achieved, attempted) = getProgramWisePLO(program1)


        return render(request, 'plostats.html', {
            'name': name,
            'usertype': type,
            'programs':programs,
            'plo': plo,
            'achieved': achieved,
            'attempted': attempted,

        })
    else:
        return render(request, 'plostats.html', {
            'name': name,
            'usertype': type,
            'programs':programs,
        })


def courseverdict(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses=[]
    for c in courselist:
        courses.append(c.courseID)


    if request.method == 'POST':

        course = request.POST['course']

        (table,total)= getVerdictTable(course)


        return render(request,'courseverdict.html',{
            'name':name,
            'usertype':type,
            'table':table,
            'courses':courses,
            'total':total,
        })




    else:
        return render(request,'courseverdict.html',{
            'name': name,
            'usertype':type,
            'courses':courses,


        })


