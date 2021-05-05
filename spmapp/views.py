from django.shortcuts import render

from .queries import *


# Create your views here.


def adminhome(request):
    return render(request, 'adminhome.html', {})


def loginview(request):
    return render(request, 'accounts/login.html', {})


def home(request):
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
    (plo,courses,table) = getCourseWisePLO(studentid)

    chartName4 = "CO-wise PLO Chart"
    (plo2,cos,table2) = getCOWisePLO(studentid)




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
        'table2': table2

    })
