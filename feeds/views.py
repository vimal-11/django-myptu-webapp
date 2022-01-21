from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from feeds.serializers import CommentsSerializer, FeedsSerializer
from .forms import PostForm, CommentForm
from .models import Feeds, Comments, Image

# Create your views here.

def index(request):
    return render(request, 'feeds/index.html')


class PostListView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Feeds.objects.filter(
            author=logged_in_user.id).order_by('-posted_on')
        form = PostForm()
        # context = {
        #     'post_list': posts,
        #     'form': form,
        # }
        serializer = FeedsSerializer(posts, many=True)
        return Response(serializer.data)
        #return render(request, 'feeds/post_list.html', context)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Feeds.objects.filter(
            author=logged_in_user.id).order_by('-posted_on')
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            for f in files:
                img = Image(image=f)
                img.save()
                new_post.image.add(img)

            new_post.save()

        # context = {
        #     'post_list': posts,
        #     'form': form,
        # }
        serializer = FeedsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return render(request, 'feeds/post_list.html', context)


class PostDetailView(LoginRequiredMixin, APIView):
    def get(self, request, pk, *args, **kwargs):
        post = Feeds.objects.get(pk=pk)
        form = CommentForm()

        comments = Comments.objects.filter(post=post).order_by('-created_on')

        # context = {
        #     'post': post,
        #     'form': form,
        #     'comments': comments,
        # }
        serializer_post = FeedsSerializer(post, many=False).data
        serializer_comments = CommentsSerializer(comments, many=True).data
        serializer = {
            'post': serializer_post,
            'comments': serializer_comments
        }

        return Response(serializer)


    def post(self, request, pk, *args, **kwargs):
        post = Feeds.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        comments = Comments.objects.filter(post=post).order_by('-created_on')

        # notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)
        # context = {
        #     'post': post,
        #     'form': form,
        #     'comments': comments,
        # }
        serializer_comments = CommentsSerializer(data=request.data)
        if serializer_comments.is_valid():
            serializer_comments.save()
            serializer_post = FeedsSerializer(post, many=False).data
            serializer_comments = CommentsSerializer(comments, many=True).data
            serializer = {
                'post': serializer_post,
                'comments': serializer_comments
            }
            return Response(serializer, status=status.HTTP_201_CREATED)
        return Response(serializer_comments.errors, status=status.HTTP_400_BAD_REQUEST)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Feeds
    fields = ['body']
    template_name = 'feeds/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
