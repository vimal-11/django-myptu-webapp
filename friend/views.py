from django.http.response import HttpResponseServerError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from authenticate.models import Account
from .models import FriendList, FriendRequest
import json

# Create your views here.

def friends_list_view(request, *args, **kwargs):
	"""
	listing all the friends of a particular user.
	Also show whether you are friends with any of the friends in that user's 
	friends list 

	Parameters
	-----------
	user = current user
	this_user = user whose friends list is viewed

	Return
	------------
	context = dictionary that has all the friends data of that particular user.
	
	context is rendered to friend/friend_list.html template. 

	"""
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Account.DoesNotExist:
				return HttpResponse("That user does not exist.")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(
					f"Could not find friends list for {this_user.username}")
			# Must be friends to view a friends list
			if user != this_user:
				if not user in friend_list.friends.all():
					return HttpResponse(
						"You must be friends to view their friends list.")
			# [(friend1, True), (friend2, False), ...]
			friends = [] 
			# get the authenticated users friend list
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, 
								auth_user_friend_list.is_mutual_friend(friend)))
			context['friends'] = friends
	else:		
		return HttpResponse("You must be friends to view their friends list.")
	return render(request, "friend/friend_list.html", context)


def friend_requests(request, *args, **kwargs):
	"""
	view for viewing all the friend requests of the user.

	Parameters
	-------------
	user = current user
	account = user whose friend requests to be viewed in detail

	Return
	-------------
	context = dictionary containing all friend requests of the particular user.

	context is rendered to friend/friend_requests.html template. 

	A user cannot view other user's friend requests.

	"""
	context = {}
	user = request.user
	if user.is_authenticated:
		user_id = kwargs.get("user_id")
		account = Account.objects.get(pk=user_id)
		if account == user:
			friend_requests = FriendRequest.objects.filter(receiver=account, 
															is_active=True)
			context['friend_requests'] = friend_requests
		else:
			return HttpResponse("You can't view another users friend requets.")
	else:
		redirect("authenticate:login")
	return render(request, "friend/friend_requests.html", context)


def send_friend_request(request, *args, **kwargs):
	"""
	Sending a friend request to a particular user.

	Method: POST

	Parameters
	------------
	receiver_user_id/user_id = user id of user who is going to receive the request.
	user = sender

	Return
	------------
	HttpResponse with JSON object to be passed into sendFriendRequest() 
	ajax function.

	"""
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				# Get any friend requests (active and not-active)
				friend_requests = FriendRequest.objects.filter(sender=user, 
															   receiver=receiver)
				# find if any of them are active (pending)
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception(
								"You already sent them a friend request.")
					# If none are active create a new friend request
					friend_request = FriendRequest(sender=user, receiver=receiver)
					friend_request.save()
					payload['response'] = "Friend request sent."
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				# There are no friend requests so create one.
				friend_request = FriendRequest(sender=user, receiver=receiver)
				friend_request.save()
				payload['response'] = "Friend request sent."
			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a friend request."
	else:
		payload['response'] = "You must be authenticated to send a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
	"""
	accepting a friend request of a particular user.
	done by calling the accept() method from the friend models.

	Method: GET

	Parameters
	------------
	friend_request_id = id of the friend request
	user = receiver of the request

	Return
	------------
	HttpResponse of a JSON object to be passed into acceptFriendRequest() 
	ajax function.

	"""
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now accept it
					updated_notification = friend_request.accept()
					payload['response'] = "Friend request accepted."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your request to accept."
		else:
			payload['response'] = "Unable to accept that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to accept a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
	"""
	unfollow / unfriending a friend from your friends list.
	done by calling the unfriend() method from the friend models.

	Method: POST

	Parameters
	------------
	removee = user who is being unfollowed or removed from friends list.
	user = user who is unfollowing

	Return
	------------
	HttpResponse of a JSON object to be passed into removeFriend() 
	ajax function.

	"""
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = Account.objects.get(pk=user_id)
				friend_list = FriendList.objects.get(user=user)
				friend_list.unfriend(removee)
				payload['response'] = "Successfully removed that friend."
			except Exception as e:
				payload['response'] = f"Something went wrong: {str(e)}"
		else:
			payload['response'] = "There was an error. Unable to remove friend."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to remove a friend."
	return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
	"""
	declining a friend request made by another user.
	done by calling the decline() method from the friend models.

	Method: GET

	Parameters
	------------
	friend_request_id = id of the friend request
	user = user who is declining.

	Return
	------------
	HttpResponse of a JSON object to be passed into declineFriendRequest() 
	ajax function.

	"""
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk=friend_request_id)
			# confirm that is the correct request
			if friend_request.receiver == user:
				if friend_request: 
					# found the request. Now decline it
					updated_notification = friend_request.decline()
					payload['response'] = "Friend request declined."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your friend request to decline."
		else:
			payload['response'] = "Unable to decline that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to decline a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
	"""
	cancelling a friend request to a friend made by the user.
	done by calling the cancel() method from the friend models.

	Method: POST

	Parameters
	------------
	receiver = user to whom the request was sent.
	user = user who is cancelling the request.

	Return
	------------
	HttpResponse of a JSON object to be passed into cancelFriendRequest() 
	ajax function.

	"""
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk=user_id)
			try:
				friend_requests = FriendRequest.objects.filter(sender=user, 
															receiver=receiver, 
															is_active=True)
			except FriendRequest.DoesNotExist:
				payload['response'] = "Nothing to cancel. Friend request does not exist."
			# There should only be ONE active friend request at any given time. 
			# Cancel them all just in case.
			if len(friend_requests) > 1:
				for request in friend_requests:
					request.cance()
				payload['response'] = "Friend request canceled."
			else:
				# found the request. Now cancel it
				friend_requests.first().cancel()
				payload['response'] = "Friend request canceled."
		else:
			payload['response'] = "Unable to cancel that friend request."
	else:
		# should never happen
		payload['response'] = "You must be authenticated to cancel a friend request."
	return HttpResponse(json.dumps(payload), content_type="application/json")