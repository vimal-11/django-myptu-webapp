from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, filters, generics
from authenticate.models import Account
from friend.models import FriendList
from feeds.serializers import CommentsSerializer, FeedsSerializer
from .forms import PostForm, CommentForm
from .models import Feeds, Comments

# Create your views here.

def index(request):
    return render(request, 'feeds/index.html')


class PostListView(LoginRequiredMixin, APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        followed_people = FriendList.objects.filter(user=logged_in_user).values('friends')
        print(followed_people)
        posts = Feeds.objects.filter(
            author__in=followed_people).order_by('-posted_on')
        # form = PostForm()
        serializer = FeedsSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        followed_people = FriendList.objects.filter(user=logged_in_user).values('friends')
        print(followed_people)
        posts = Feeds.objects.filter(
            author__in=followed_people).order_by('-posted_on')
        # form = PostForm(request.POST, request.FILES)
        # files = request.FILES.getlist('image')

        # if form.is_valid():
        #     new_post = form.save(commit=False)
        #     new_post.author = request.user
        #     new_post.save()

        #     for f in files:
        #         img = Image(image=f)
        #         img.save()
        #         new_post.image.add(img)

        #     new_post.save()

        # context = {
        #     'post_list': posts,
        #     'form': form,
        # }
        print(request, request.POST, request.FILES)
        print("data: ",request.data)
        # image = request.data['image']
        # del request.data['image']
        # request.data['image'] = []
        # for img in image:
        #     img_model = Image.objects.create(image=img)
        #     img_model.save()
        #     request.data['image'].append(img_model.id)
        # print("image model: ", request.data)
        serializer = FeedsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer = FeedsSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class OwnerPostsView(LoginRequiredMixin, APIView):
    def get(self, request, user_id=None):
        user = request.user
        try:
            owner = Account.objects.get(pk=user_id)
        except:
            return HttpResponse("Something went wrong.")
        if user.is_authenticated and user == owner:
            posts = Feeds.objects.filter(
                                 author=owner.id).order_by('-posted_on')
            serializer = FeedsSerializer(posts, many=True)
            return Response(serializer.data)
        return HttpResponse("you are not authorized to this view.")


class PostEditView(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    serializer_class = FeedsSerializer
    queryset = Feeds.objects.all()

    def get_queryset(self, *args, **kwargs):
        post = self.kwargs['pk']
        post_author = Feeds.objects.get(pk = post).author
        print(post_author, self.request.user)
        if post_author == self.request.user:
            queryset = Feeds.objects.filter(author=self.request.user.id).order_by('-posted_on')
            return queryset


class PostDeleteView(LoginRequiredMixin, generics.RetrieveDestroyAPIView):
    serializer_class = FeedsSerializer
    queryset = Feeds.objects.all()

    def get_queryset(self, *args, **kwargs):
        post = self.kwargs['pk']
        post_author = Feeds.objects.get(pk = post).author
        print(post_author, self.request.user)
        if post_author == self.request.user:
            queryset = Feeds.objects.filter(author=self.request.user.id).order_by('-posted_on')
            return queryset

'''
RetrieveDestroyAPIView:
----------------------
Used for read or delete endpoints to represent a single model instance.
Provides get and delete method handlers.
Extends: GenericAPIView, RetrieveModelMixin, DestroyModelMixin

RetrieveUpdateAPIView:
----------------------
Used for read or update endpoints to represent a single model instance.
Provides get, put and patch method handlers.
Extends: GenericAPIView, RetrieveModelMixin, UpdateModelMixin

'''

