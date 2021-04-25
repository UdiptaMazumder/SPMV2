from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def adminhome(request):
    return render(request, 'adminhome.html', {})

def new(request):
    return render(request,'new.html', {})