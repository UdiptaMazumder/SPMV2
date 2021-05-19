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

# list

schoollist = School_T.objects.all()
deptlist = Department_T.objects.all()
programlist = Program_T.objects.all()
courselist = Course_T.objects.all()
sectionlist = Section_T.objects.all()
faculties = Faculty_T.objects.all()
semlist = getAllSemesters()

semesters = []

for s in semlist:
    semesters.append(s[0])


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

    chart3 = "Student Wise Gpa"
    gpalabel1 = []
    gpadata1 = []

    for s in semesters:
        print(s)
        gpalabel1.append(s)
        gpadata1.append(getStudentWiseGPA(studentid, s))

    chart4 = "Department Wise Gpa"
    gpalabel2 = []
    gpadata2 = []

    for s in semesters:
        gpalabel2.append(s)
        gpadata2.append(getDeptWiseGPA(dept, s))

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

    for s in semesters:
        gpadata.append(getDeptWiseGPA(dept, s))
        gpalabel.append(s)

    return render(request, 'facultyhome.html', {
        'name': name,
        'usertype': type,

        'plolabel': plolabel,
        'plodata': plodata,
        'gpalabel': gpalabel,
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

    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    schools = []
    depts = []
    programs = []
    programnames = []

    for s in schoollist:
        schools.append(s.schoolID)

    for d in deptlist:
        depts.append(d.departmentID)

    for p in programlist:
        programs.append(p.programID)
        programnames.append(p.programName)

    gpalabel = []

    for s in semesters:
        gpalabel.append(s)

    # schoolwise gpa
    sgpatable = []

    for school in schools:
        gpa = []

        for s in semesters:
            gpa.append(getSchoolWiseGPA(school, s))

        sgpatable.append(gpa)

    # deptwise gpa
    dgpatable = []

    for dept in depts:
        gpa = []

        for s in semesters:
            gpa.append(getDeptWiseGPA(dept, s))

        dgpatable.append(gpa)

    # programwise gpa
    pgpatable = []

    for p in programs:
        gpa = []
        for s in semesters:
            gpa.append(getProgramWiseGPA(p, s))
        pgpatable.append(gpa)

    return render(request, 'hahome.html', {
        'name': name,
        'usertype': type,

        'gpalabel': gpalabel,

        'schools': schools,
        'sgpatable': sgpatable,

        'depts': depts,
        'dgpatable': dgpatable,

        'programs': programnames,
        'pgpatable': pgpatable,

        'totalstudents': totalStudents,

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
            'sid': studentid,

            'search': 0,
        }

        return render(request, 'plo.html', response)
    else:
        return render(request, 'plo.html', {
            'name': name,
            'usertype': type,
            'sid': None,
            'search': 1
        })


def enrollment(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        schools = []
        depts = []
        programs = []
        programnames = []

        for s in schoollist:
            schools.append(s.schoolID)

        for d in deptlist:
            depts.append(d.departmentID)

        for p in programlist:
            programs.append(p.programID)
            programnames.append(p.programName)

        # schoolwise students
        snum = []
        for school in schools:
            num = 0

            for i in range(b, e + 1):
                num += getSchoolWiseEnrolledStudents(school, semesters[i])
            snum.append(num)

        # deptwise students
        dnum = []

        for dept in depts:
            num = 0

            for i in range(b, e + 1):
                num += getDeptWiseEnrolledStudents(dept, semesters[i])
            dnum.append(num)

        # programwise students
        pnum = []

        for p in programs:
            num = 0

            for i in range(b, e + 1):
                num += getProgramWiseEnrolledStudents(p, semesters[i])
            pnum.append(num)

        return render(request, 'enrollment.html', {
            'name': name,
            'usertype': type,

            'school': schools,
            'snum': snum,
            'depts': depts,
            'dnum': dnum,
            'program': programnames,
            'pnum': pnum,
            'semesters': semesters,
            'selected1': b,
            'selected2': e,
            'search': 0,
        })
    else:
        return render(request, 'enrollment.html', {
            'name': name,
            'usertype': type,
            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'search': 1,
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
            'sid': studentid,
            'search': 0,

        })
    else:
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'sid': None,
            'search': 1,
        })


def plostats(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        prog = int(request.POST['program'])

        (plo, achieved, attempted) = getProgramWisePLO(prog)

        return render(request, 'plostats.html', {
            'name': name,
            'usertype': type,
            'programs': programlist,
            'plo': plo,
            'achieved': achieved,
            'attempted': attempted,
            'selectedItem': prog,
            'search': 0,

        })
    else:
        return render(request, 'plostats.html', {
            'name': name,
            'usertype': type,
            'programs': programlist,
            'selectedItem': None,
            'search': 1,
        })


def courseverdict(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []
    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':

        course = request.POST['course']

        (table, total) = getVerdictTable(course)

        return render(request, 'courseverdict.html', {
            'name': name,
            'usertype': type,
            'table': table,
            'courses': courses,
            'total': total,
            'search': 0,
            'selectedCourse': course,

        })

    else:
        return render(request, 'courseverdict.html', {
            'name': name,
            'usertype': type,
            'courses': courses,
            'search': 1,
            'selectedCourse': None,

        })


def dataentry2(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []
    for c in courselist:
        courses.append(c.courseID)

    semesters = ["Spring", "Summer", "Autumn"]

    sections = [1, 2, 3]
    year = [2019, 2020]

    return render(request, 'dataentry2.html', {
        'name': name,
        'usertype': type,
        'courses': courses,
        'semesters': semesters,
        'sections': sections,
        'year': year,
    })

####def dataentry(request):
 ####   name = request.user.get_full_name()
####    type = request.user.groups.all()[0].name

####    courses = []
####    for c in courselist:
 ####       courses.append(c.courseID)

 ####   semesters = ["Spring", "Summer", "Autumn"]

 ####   sections = [1, 2, 3]
####    year = [2019, 2020]

 ####   return render(request, 'dataentry2.html', {
 ####       'name': name,
 ####       'usertype': type,
 ####       'courses': courses,
 ####       'semesters': semesters,
 ####       'sections': sections,
  ####      'year': year,
 ####   })

def semesterwisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    schools = []
    depts = []
    programs = []
    programnames = []

    for s in schoollist:
        schools.append(s.schoolID)

    for d in deptlist:
        depts.append(d.departmentID)

    for p in programlist:
        programs.append(p.programID)
        programnames.append(p.programName)

    if request.method == "POST":
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        labels = []

        for i in range(b, e + 1):
            labels.append(semesters[i])

        # schoolwise gpa
        sgpatable = []

        for school in schools:

            gpa = []

            for i in range(b, e + 1):
                gpa.append(getSchoolWiseGPA(school, semesters[i]))

            sgpatable.append(gpa)

        # deptwise gpa
        dgpatable = []

        for dept in depts:
            gpa = []

            for i in range(b, e + 1):
                gpa.append(getDeptWiseGPA(dept, semesters[i]))

            dgpatable.append(gpa)

        # programwise gpa
        pgpatable = []

        for p in programs:
            gpa = []
            for i in range(b, e + 1):
                gpa.append(getProgramWiseGPA(p, semesters[i]))

            pgpatable.append(gpa)

        return render(request, 'semesterwisegpa.html', {
            'name': name,
            'usertype': type,

            'semesters': semesters,
            'selected1': b,
            'selected2': e,

            'schools': schools,
            'sgpatable': sgpatable,
            'labels': labels,

            'depts': depts,
            'dgpatable': dgpatable,

            'programs': programnames,
            'pgpatable': pgpatable,

            'search': 0,

        })
    else:
        return render(request, 'semesterwisegpa.html', {
            'name': name,
            'usertype': type,

            'semesters': semesters,

            'selected1': None,
            'selected2': None,
            'search': 1,

        })


def coursewisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []

    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':
        selectedCourses = request.POST.getlist('courses')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        label = []

        for i in range(b, e + 1):
            label.append(semesters[i])

        gpatable = []

        for c in selectedCourses:
            gpa = []
            for i in range(b, e + 1):
                gpa.append(getCourseWiseGPA(c, semesters[i]))
            gpatable.append(gpa)

        return render(request, 'coursewisegpa.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,

            'selected1': b,
            'selected2': e,
            'selectedCourses': selectedCourses,

            'gpatable': gpatable,
            'labels': label,

            'search': 0,

        })

    else:
        return render(request, 'coursewisegpa.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'search': 1,
        })


def instructorwisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        selectedIns = request.POST.getlist('instructors')

        fnames = []

        for i in range(0, len(selectedIns)):
            selectedIns[i] = int(selectedIns[i])
            for j in faculties:
                if j.facultyID == selectedIns[i]:
                    fnames.append(j.firstName + " " + j.lastName)

        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        label = []

        for i in range(b, e + 1):
            label.append(semesters[i])

        gpatable = []

        for s in selectedIns:
            gpa = []
            for i in range(b, e + 1):
                gpa.append(getInstructorWiseGPA(s, semesters[i]))
            gpatable.append(gpa)

        return render(request, 'inswisegpa.html', {
            'name': name,
            'usertype': type,

            'instructors': faculties,
            'fnames': fnames,
            'semesters': semesters,

            'selected1': b,
            'selected2': e,
            'selectedIns': selectedIns,

            'gpatable': gpatable,
            'labels': label,
            'search': 0,

        })

    else:
        return render(request, 'inswisegpa.html', {
            'name': name,
            'usertype': type,

            'instructors': faculties,

            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'selectedIns': None,
            'search': 1,
        })


def instructorwisegpaforcourse(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []

    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':
        selectedCourse = request.POST['course']
        b = int(request.POST['sem1'])
        end = int(request.POST['sem2'])


        label = []

        for i in range(b, end + 1):
            label.append(semesters[i])

        gpatable = []
        ins = []
        insnames = []
        temp = []

        for i in range(b, end + 1):
            temp.append(getInstructorWiseGPAForCourse(selectedCourse, semesters[i]))
        print(temp)

        for t in temp:
            for e in t:
                if e[0] not in ins:
                    ins.append(e[0])

        for i in ins:
            for f in faculties:
                if f.facultyID == i:
                    insnames.append(f.firstName+" "+f.lastName)
            gpa = []
            for t in temp:
                for e in t:
                    if e[0] == i:
                        gpa.append(e[1])
            gpatable.append(gpa)

        return render(request, 'instructorwisegpaforcourse.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,

            'selected1': b,
            'selected2': end,
            'selectedCourse': selectedCourse,

            'gpatable': gpatable,
            'labels': label,
            'ins': ins,
            'insnames':insnames,

            'search': 0,

        })

    else:
        return render(request, 'instructorwisegpaforcourse.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'search': 1,
        })


def leaderwisegpa(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    headlist = Head_T.objects.all()
    deanlist = Dean_T.objects.all()
    vclist = VC_T.objects.all()

    headlabel = []
    headgpa = []

    deanlabel = []
    deangpa = []

    vclabel = []
    vcgpa = []

    for h in headlist:
        headlabel.append(h.firstName + " " + h.lastName)
        headgpa.append(getHeadWiseGPA(h))

    for d in deanlist:
        deanlabel.append(d.firstName + " " + d.lastName)
        deangpa.append(getDeanWiseGPA(d))

    for v in vclist:
        vclabel.append(v.firstName + " " + v.lastName)
        vcgpa.append(getVCWiseGPA(v))

    return render(request, 'leaderwisegpa.html', {
        'name': name,
        'usertype': type,

        'headlabel': headlabel,
        'headgpa': headgpa,

        'deanlabel': deanlabel,
        'deangpa': deangpa,

        'vclabel': vclabel,
        'vcgpa': vcgpa,
    })
