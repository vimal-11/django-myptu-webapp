from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, filters, generics
from authenticate.models import Account
from friend.models import FriendList
from feeds.serializers import CommentsSerializer, FeedsSerializer
from .models import Feeds, Comments

# Create your views here.

class PostListView(LoginRequiredMixin, APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        followed_people = FriendList.objects.filter(
                                    user=logged_in_user).values('friends')
        print(followed_people)
        posts = Feeds.objects.filter(
                              author__in=followed_people).order_by('-posted_on')
        # form = PostForm()
        serializer = FeedsSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        logged_in_user = request.user
        followed_people = FriendList.objects.filter(
                                    user=logged_in_user).values('friends')
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
        print(request, request.POST, request.FILES, request.data)
        if 'author' not in request.data.keys():
            request.data['author'] = logged_in_user.id
        # image = request.data['image']
        # del request.data['image']
        # request.data['image'] = []
        # for img in image:
        #     img_model = Image.objects.create(image=img)
        #     img_model.save()
        #     request.data['image'].append(img_model.id)
        # print("image model: ", request.data)
        if logged_in_user.id == request.data['author'] or logged_in_user == request.data['author']:
            serializer = FeedsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                serializer = FeedsSerializer(posts, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("You don't have access.", status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(LoginRequiredMixin, APIView):
    def get(self, request, pk, *args, **kwargs):
        post = Feeds.objects.get(pk=pk)
        #form = CommentForm()
        comments = Comments.objects.filter(post=post).order_by('-created_on')
        serializer_post = FeedsSerializer(post, many=False).data
        serializer_comments = CommentsSerializer(comments, many=True).data
        serializer = {
            'post': serializer_post,
            'comments': serializer_comments
        }
        return Response(serializer)


    def post(self, request, pk, *args, **kwargs):
        post = Feeds.objects.get(pk=pk)
        # need to check for post and author of the comment...pending
        comments = Comments.objects.filter(post=post).order_by('-created_on')
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
        return Response("you are not authorized to this view.", 
                                            status=status.HTTP_400_BAD_REQUEST)


class PostCreateView(LoginRequiredMixin, generics.CreateAPIView):
    """
    Concrete view for creating a model instance.
    """
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = FeedsSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostEditView(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    """
        Concrete view for retrieving, updating a model instance.
    """
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = FeedsSerializer
    queryset = Feeds.objects.all()

    def get_queryset(self, *args, **kwargs):
        post = self.kwargs['pk']
        post_author = Feeds.objects.get(pk = post).author
        print(post_author, self.request.user)
        if post_author == self.request.user:
            queryset = Feeds.objects.filter(
                              author=self.request.user.id).order_by('-posted_on')
            return queryset


class PostDeleteView(LoginRequiredMixin, generics.RetrieveDestroyAPIView):
    serializer_class = FeedsSerializer
    queryset = Feeds.objects.all()

    def get_queryset(self, *args, **kwargs):
        post = self.kwargs['pk']
        post_author = Feeds.objects.get(pk = post).author
        print(post_author, self.request.user)
        if post_author == self.request.user:
            queryset = Feeds.objects.filter(
                              author=self.request.user.id).order_by('-posted_on')
            return queryset


class CommentCreateView(LoginRequiredMixin, generics.ListCreateAPIView):
    """
        Concrete view for retrieving, updating a model instance.
    """
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

    def get_queryset(self, *args, **kwargs):
        post = self.kwargs['post_id']
        queryset = Comments.objects.filter(post=post)
        print(self.request.user.id, queryset, self.kwargs)
        return queryset

    def post(self, request, *args, **kwargs):
        post = kwargs.get('post_id')
        print(post, request.data['author'], request.data['comment'], 
                                            request.data['post'], request.user.id)
        if str(post) != str(request.data['post']) or str(request.user.id) != str(request.data['author']):
            return Response("you are not authorized for this comment.", 
                                              status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)
    

class CommentEditView(LoginRequiredMixin, generics.RetrieveUpdateAPIView):
    """
        Concrete view for retrieving, updating a model instance.
    """
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

    def get_queryset(self, *args, **kwargs):
        post = self.kwargs['post_id']
        queryset = Comments.objects.filter(author=self.request.user.id, post=post)
        print(self.request.user.id, queryset, self.kwargs)
        return queryset


class CommentDeleteView(LoginRequiredMixin, generics.DestroyAPIView):
    """
        Concrete view for deleting a model instance.
    """
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

    def get_queryset(self, *args, **kwargs):
        post = self.kwargs['post_id']
        queryset = Comments.objects.filter(author=self.request.user.id, post=post)
        print(self.request.user.id, queryset, self.kwargs)
        return queryset



'''
CreateAPIView
--------------------
Used for create-only endpoints.
Provides a post method handler.
Extends: GenericAPIView, CreateModelMixin

ListCreateAPIView
----------------------
Used for read-write endpoints to represent a collection of model instances.
Provides get and post method handlers.
Extends: GenericAPIView, ListModelMixin, CreateModelMixin

RetrieveDestroyAPIView
----------------------
Used for read or delete endpoints to represent a single model instance.
Provides get and delete method handlers.
Extends: GenericAPIView, RetrieveModelMixin, DestroyModelMixin

RetrieveUpdateAPIView
----------------------
Used for read or update endpoints to represent a single model instance.
Provides get, put and patch method handlers.
Extends: GenericAPIView, RetrieveModelMixin, UpdateModelMixin

DestroyAPIView
----------------------
Used for delete-only endpoints for a single model instance.
Provides a delete method handler.
Extends: GenericAPIView, DestroyModelMixin

https://github.com/encode/django-rest-framework/blob/master/rest_framework/generics.py
'''

