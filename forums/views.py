from decimal import Context
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

from authenticate.models import Account
from .models import Category, Query, Reply
from . utils import update_views
from .forms import NewQuery
# Create your views here.

def forum(request):
    topics = Category.objects.all()
    paginator = Paginator(topics, 3)
    page = request.GET.get("page")
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    context = {
        "topics":topics,
    }
    return render(request, "forums/forum.html", context)

def topic(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queries = Query.objects.filter(approved=True, categories=category)
    paginator = Paginator(queries, 5)
    page = request.GET.get("page")
    try:
        queries = paginator.page(page)
    except PageNotAnInteger:
        queries = paginator.page(1)
    except EmptyPage:
        queries = paginator.page(paginator.num_pages)

    context = {
        "topic_queries":queries,
        "catgr": category,
    }
    return render(request, "forums/forum_posts.html", context)

    
@login_required(login_url="authenticate:login")
def query(request, slug):
    question = get_object_or_404(Query, slug=slug)
    r_user = Account.objects.get(username = request.user.username)
    print("rply start! \n")

    if "submit_reply" in request.POST:
        rply = request.POST.get("reply")
        print("rely: ", rply, "\n")
        new_reply, created = Reply.objects.get_or_create(user=r_user, reply=rply)
        question.replies.add(new_reply.id)


    context = {
        "query":question
    }
    update_views(request, question)
    return render(request, "forums/post_detail.html", context)


@login_required(login_url="authenticate:login")
def newquery(request):
    context = {}
    form = NewQuery(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            q_user = Account.objects.get(username = request.user.username)
            new_query = form.save(commit=False)
            new_query.user = q_user
            new_query.save()
            return redirect("forums:forum")
    context.update({
        "form": form,
        "title": "New Query"
    })
    return render(request, "forums/new_query.html", context)


def search_results(request):
    context = {}
    
    
    if "search-sub" in request.GET:
        keyword = request.GET.get("keyword")
        #filter starting
        
        search_box = request.GET.get("search-box")
        if search_box == "title":
            results = Query.objects.all()
            objects = Query.objects.filter(title__contains = keyword)
           
        elif search_box == "category":
            results = Category.objects.all()
            objects = Category.objects.filter(title__contains = keyword)
        

        #ends
        paginator = Paginator(objects, 1)
        page = request.GET.get("page")
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        


        print("\n\n")
        print(keyword)
        for obj in objects:
            print(obj)

        context = {
            "objects": objects,
            "searched": keyword,
            "search_box":search_box,
            "results":results,
        }
    return render(request, "forums/search.html", context)