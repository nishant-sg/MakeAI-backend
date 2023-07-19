from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import testUser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test(request):
    return HttpResponse("The API is Succefully working!!!")

@csrf_exempt
def create(request):
    if request.method=="POST":
        print("---------------------------------",request.POST)
        name=request.POST['name']
        age=request.POST['age']
        obj=testUser.objects.create(name=name,age=age)
        obj.save()
        # return redirect('/test')
        return HttpResponse("Test User Created Successfully!!!")
    