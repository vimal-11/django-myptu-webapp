from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import HttpResponse
import workshops
from .models import Workshop,Registered_workshop
# Create your views here.

def ListView(request):
    workshop = get_object_or_404(Workshop,id=1)
    context = {}
    context["list"] = Workshop.objects.all()
    return render(request,'workshops/list_workshop.html',context)

    
