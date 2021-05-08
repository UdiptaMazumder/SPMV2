from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


from .queries import *


# Create your views here.

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

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})

def logoutview(request):
    logout(request)
    return redirect('loginview')



def adminhome(request):
    return render(request, 'adminhome.html', {})



@login_required(login_url="/login/")
def home(request):
    name = request.user.get_full_name()
    studentid = 1416455
    row = getStudentWiseOverallPLO(studentid)
    chartName = 'PLO Achievement'
    chartLabel = []
    chartDataSet = []

    chartName2 = "Semester Wise Gpa"
    chartLabel2 = []
    chartDataSet2 = []
    row2 = []

    row2.append(getStudentWiseGpa(1823228, "Spring", 2020))
    row2.append(getStudentWiseGpa(1823228, "Summer", 2020))
    row2.append(getStudentWiseGpa(1823228, "Autumn", 2020))

    chartName3 = "Course-wise PLO Chart"
    (plo,courses,table) = getCourseWisePLO(studentid,"chart")

    chartName4 = "CO-wise PLO Chart"
    (plo2,cos,table2) = getCOWisePLO(studentid,"chart")


    for i in row:
        chartLabel.append(i[0])
        chartDataSet.append(i[1])

    for i in row2:
        chartLabel2.append(i[0])
        chartDataSet2.append(i[1])

    return render(request, 'index.html', {
        'chartName': chartName,
        'chartLabel': chartLabel,
        'chartDataSet': chartDataSet,

        'chartName2': chartName2,
        'chartLabel2': chartLabel2,
        'chartDataSet2': chartDataSet2,

        'chartName3': chartName3,
        'plo': plo,
        'courses': courses,
        'table': table,

        'chartName4': chartName4,
        'plo2': plo2,
        'cos': cos,
        'table2': table2,
        'name': name

    })

def userprofile(request):
    return render(request,'page-user.html', {})
