from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.



def hello_world(self):
    return HttpResponse("Hello world")



def home(request):
    return render(request, 'applications/home.html')