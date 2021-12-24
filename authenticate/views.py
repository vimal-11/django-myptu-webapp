from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import modelformset_factory
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from PTU import settings

from authenticate.forms import UserRegisterForm
from authenticate.models import users
from friend.models import FriendList, FriendRequest
from friend.request_status import FriendRequestStatus
from friend.utils import get_friend_request_or_false
from . tokens import generate_token


# Create your views here.

def home(request):
    return render(request, "authenticate/home.html")

def signup(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('create_password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()

            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.is_active = False

            new_user.save()

            messages.success(request, 'Registered Successfully!')
            
           
            #Confirmation mail

            current_site = get_current_site(request)
            email_subject = "MYPTU - Confirmation Mail!"
            message = render_to_string('email_confirmation.html',{
                    'name': new_user.first_name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token': generate_token.make_token(new_user)
            })
            email = EmailMessage(
                email_subject, 
                message,
                settings.EMAIL_HOST_USER,
                [new_user.email],
            )
            email.fail_silently = True
            email.send()

            return render(request, 'authenticate/index.html', {'name': new_user.first_name})
    else:
            form = UserRegisterForm()

    return render(request, 'authenticate/signup.html', {'form': form})

        
    
def loginUser(request):

    if request.method == 'POST':
        username = request.POST['username'] 
        pass1 = request.POST['password']
        #print(username,type(username), pass1, type(pass1) )
        if "@" in username:
            user_cred = User.objects.get(email=username.lower()).username
        else:
            user_cred = username
    
        user = authenticate(request, username=user_cred, password=pass1)
        
        print(user, type(user))
        
        if user is not None:
            login(request, user)
            fname = user.first_name

            if 'next' in request.POST:
                return redirect(request.POST.get('next')) 
            else:
                return redirect('authenticate:profilepage', pk=user.pk)
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('authenticate:home')


    return render(request, 'authenticate/login.html')
    
@login_required
def logoutUser(request):
    #if request.method == 'POST':
    logout(request)
    return redirect('authenticate:home')
    #return redirect('authenticate:login')

def index(request):
    return render(request, 'authenticate/index.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        return redirect('authenticate:login')
    else:
        return HttpResponse("Activation Failed!")


class profile_view(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        context = {}
        try:
            user_acc = User.objects.get(pk=pk)
        except:
            return HttpResponse("Something went wrong.")
        
        if user_acc:
            context['id'] = user_acc.id
            context['username'] = user_acc.username
            context['email'] = user_acc.email

            try:
                friend_list = FriendList.objects.get(user=user_acc)
            except FriendList.DoesNotExist:
                friend_list = FriendList(user=user_acc)
                friend_list.save()
            friends = friend_list.friends.all()
            context['friends'] = friends

            # Define template variables
            is_self = True
            is_friend = False
            request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
            friend_requests = None
            user = request.user
            if user.is_authenticated and user != user_acc:
                is_self = False
                if friends.filter(pk=user.id):
                    is_friend = True
                else:
                    is_friend = False
                    # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                    if get_friend_request_or_false(sender=user_acc, receiver=user) != False:
                        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                        context['pending_friend_request_id'] = get_friend_request_or_false(sender=user_acc, receiver=user).id
                    # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                    elif get_friend_request_or_false(sender=user, receiver=user_acc) != False:
                        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                    # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                    else:
                        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            elif not user.is_authenticated:
                is_self = False
            else:
                try:
                    friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
                except:
                    pass
                
            # Set the template variables to the values
            context['is_self'] = is_self
            context['is_friend'] = is_friend
            context['request_sent'] = request_sent
            context['friend_requests'] = friend_requests
            #context['BASE_URL'] = settings.BASE_URL
        return render(request, 'authenticate/profilepage.html', context)
    