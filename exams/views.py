from django.db.models import fields
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Exam, Exam_Detail, Pyqs
#from . import data

def exam(request, slug):
    exam = get_object_or_404(Exam, slug=slug)
    fields = Exam_Detail.objects.filter(exam = exam)
    context = {'fields': fields, 'exam': exam}
    return render (request, 'exams/upsc.html', context)



'''def examupdate(request):
    update = data.UPSC()
    return redirect('http://127.0.0.1:8000/admin/exams')'''
    



def exam_detail(request, exam_slug, field_slug):
    exams = [c.slug for c in Exam.objects.all()]
    if exam_slug in exams:
        exam_match = Exam.objects.get(slug = exam_slug)
        fields = [k.slug for k in Exam_Detail.objects.filter(exam = exam_match)]
        if field_slug in fields:
            field_match = Exam_Detail.objects.filter(slug = field_slug).values_list('id', 'field')
            field = get_object_or_404(Exam_Detail, slug=field_slug)
            pyq = list(Pyqs.objects.filter(exam_field = field).values('year', 'year_slug'))
            for k in pyq:
                c = k
                for p in pyq[pyq.index(k)+1:]:
                    if p == c:
                        pyq.remove(p)
            #print(pyq, len(pyq)) 
            context = {
                'field_match': field_match,
                'field': field,
                'pyqs': pyq
            }
            return render (request, 'exams/exam_detail.html', context)
        else:
            return redirect("http://127.0.0.1:8000/")
    return redirect("http://127.0.0.1:8000/")




def pyqs(request, exam_slug, field_slug, year_slug):
    objs = Pyqs.objects.filter(exam = Exam.objects.get(slug = exam_slug).id, exam_field = Exam_Detail.objects.get(slug=field_slug).id, year_slug = year_slug ).values('phase')
    obj = list(objs)
    for k in obj:
                c = k
                for p in obj[obj.index(k)+1:]:
                    if p == c:
                        obj.remove(p)
    print(obj, len(obj))
    cag = []
    for k in obj:
        catg = objs.filter(phase = k['phase'])
        cat = list((catg).values('category', 'subject', 'link'))
        print(cat, len(cat))
        cag.append(cat)
    zip_obj = zip(obj, cag)
    context = {
        'objects': obj,
        'category': zip_obj,
        'year': year_slug
        }
    return render (request, 'exams/pyqs.html', context)