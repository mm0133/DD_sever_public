from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.


def foo(request):
    return HttpResponse("You're looking at question %s." )
