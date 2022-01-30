from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from .models import Workshop,Registered_workshop

# Create your views here.

def ListView(request):
    #workshop = get_object_or_404(Workshop,id=1)
    workshop_list = Workshop.objects.all()
    paginator = Paginator(workshop_list, 20)
    page = request.GET.get('page')
    #page = int(page)
    #print(type(page))
    #print(page)
    page_obj = Paginator.get_page(paginator,page)
    return render(request,'workshops/list_workshop.html',{'page_obj':page_obj})

    
