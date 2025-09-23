from django.http import HttpResponse
from django.shortcuts import render


def homePage(request):
    return render(request,'home.html')
    #return HttpResponse("Hello, world. You're at the polls page.")

def about(request):
    return render(request, 'about.html')