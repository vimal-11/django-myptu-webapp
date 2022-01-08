from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views import View
from authenticate.models import Account
from django.contrib import messages
from django.forms import modelformset_factory
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from PTU import settings
from django.conf import settings

from authenticate.forms import AccountUpdateForm, UserRegisterForm
from friend.models import FriendList, FriendRequest
from friend.request_status import FriendRequestStatus
from friend.utils import get_friend_request_or_false
from . tokens import generate_token


# Create your views here.


def home(request):
    return render(request, "authenticate/home.html")


def account_search_view(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_results = Account.objects.filter(
                        email__icontains=search_query).filter(
                            username__icontains=search_query).distinct()
			user = request.user
			accounts = [] # [(account1, True), (account2, False), ...]
			if user.is_authenticated:
				# get the authenticated users friend list
				auth_user_friend_list = FriendList.objects.get(user=user)
				for account in search_results:
					accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
				context['accounts'] = accounts
			else:
				for account in search_results:
					accounts.append((account, False))
				context['accounts'] = accounts
				
	return render(request, "authenticate/search.html", context)



def signup(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated: 
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            form.save()

            new_user = Account.objects.get(email=email, username=username)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.is_active = False

            new_user.save()

            messages.success(request, 'Registered Successfully!')

            # Confirmation mail
            current_site = get_current_site(request)
            print(current_site)
            email_subject = "MYPTU - Confirmation Mail!"
            message = render_to_string('email_confirmation.html', 
                {
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
            return render(request, 'authenticate/index.html', 
                                        {'name': new_user.first_name})
        else:
            context['registration_form'] = form
    else:
        form = UserRegisterForm()
        context['registration_form'] = form
    return render(request, 'authenticate/signup.html', context)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        if "@" in username:
            user_cred = Account.objects.get(email=username.lower()).username
        else:
            user_cred = username
        user = authenticate(request, username=user_cred, password=pass1)
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
    # if request.method == 'POST':
    logout(request)
    return redirect('authenticate:home')


def index(request):
    return render(request, 'authenticate/index.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        new_user = Account.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        new_user = None
    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        return redirect('authenticate:login')
    else:
        return HttpResponse("Activation Failed!")


class profile_view(LoginRequiredMixin, View):
    """
	- Logic here is kind of tricky
		is_self
		is_friend
			-1: NO_REQUEST_SENT
			0: THEM_SENT_TO_YOU
			1: YOU_SENT_TO_THEM
	"""
    def get(self, request, pk=None):
        context = {}
        try:
            user_acc = Account.objects.get(pk=pk)
        except:
            return HttpResponse("Something went wrong.")
        
        if user_acc:
            context['id'] = user_acc.id
            context['username'] = user_acc.username
            context['email'] = user_acc.email
            context['profile_image'] = user_acc.profile_image.url
            context['hide_email'] = user_acc.hide_email

            try:
                friend_list = FriendList.objects.get(user=user_acc)
            except FriendList.DoesNotExist:
                friend_list = FriendList.objects.create(user=user_acc)
                friend_list.save()
            friends = friend_list.friends.all()
            context['friends'] = friends

            # Define template variables
            is_self = True
            is_friend = False
            # range: ENUM -> friend/friend_request_status.FriendRequestStatus
            request_sent = FriendRequestStatus.NO_REQUEST_SENT.value 
            friend_requests = None
            user = request.user
            if user.is_authenticated and user != user_acc:
                is_self = False
                if friends.filter(pk=user.id):
                    is_friend = True
                else:
                    is_friend = False

                    # CASE1: Request has been sent from THEM to YOU: 
                    # FriendRequestStatus.THEM_SENT_TO_YOU
                    if get_friend_request_or_false(sender=user_acc, receiver=user) != False:
                        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                        context['pending_friend_request_id'] = get_friend_request_or_false(
                                                                sender=user_acc,
                                                                receiver=user).id

                    # CASE2: Request has been sent from YOU to THEM: 
                    # FriendRequestStatus.YOU_SENT_TO_THEM
                    elif get_friend_request_or_false(sender=user, receiver=user_acc) != False:
                        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value

                    # CASE3: No request sent from YOU or THEM: 
                    # FriendRequestStatus.NO_REQUEST_SENT
                    else:
                        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            elif not user.is_authenticated:
                is_self = False
            else:
                try:
                    friend_requests = FriendRequest.objects.filter(receiver=user, 
                                                                is_active=True)
                except:
                    pass

            # Set the template variables to the values
            context['is_self'] = is_self
            context['is_friend'] = is_friend
            context['request_sent'] = request_sent
            context['friend_requests'] = friend_requests
            context['BASE_URL'] = settings.BASE_URL
        print(context)
        return render(request, 'authenticate/profilepage.html', context)
    

def edit_account_view(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("authenticate:login")
	user_id = kwargs.get("user_id")
	account = Account.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect("authenticate:profilepage", pk=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"first_name": account.first_name,
					"last_name": account.last_name,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"first_name": account.first_name,
					"last_name": account.last_name,
				}
			)
		context['form'] = form
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "authenticate/edit_account.html", context)