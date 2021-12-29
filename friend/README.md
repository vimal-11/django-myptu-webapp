# Friend System

## Profile View

The profile view of an user must rendered properly according to the status of the friend requests. There are three possible types of views according to the status of requests

> 1. View for **No Request Sent**  
> &nbsp;&nbsp;&nbsp;&nbsp;a. If user != owner  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i.If user is not a friend   
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Enable _Send friend request_   
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Else    
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1. Enable _Remove friend_  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Else  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. view all friends  
>   
> 2. View for request sent from **Them to You**  
> &nbsp;&nbsp;&nbsp;&nbsp;a. If user != owner  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Enable _Accept friend request_  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Enable _Decline friend request_  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Else  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Enable _friend request list_  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. List all friend requests  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Enable _Accept and Decline friend requests_  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. view all friends  
>   
> 3. View for request sent from **You to Them**  
> &nbsp;&nbsp;&nbsp;&nbsp;a. If user != owner  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Enable _Cancel friend Request_  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Else  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. view all friends 
  
  
## Send Friend Request  

Sending a friend request to a particular user.


### Algorithm: send_friend_request(request, *args, **kwargs)

> 1. Get the current user (i.e request.user).  
> 2. If the method is POST and current user is authenticated:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Get the ‘receiver_user_id’ from POST request  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Obtain receiver of the friend request from the AUTH_USER_MODEL using receiver_user_id.  
> &nbsp;&nbsp;&nbsp;&nbsp;c. If there exist any friend requests (active or non-active) between user and receiver in the database:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. If friend request is active:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Notify user that a friend request has been already sent.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Create a friend request with sender=user and receiver=receiver.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Save the friend request in the database.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Response = ‘Friend request sent’  
> &nbsp;&nbsp;&nbsp;&nbsp;d. Else if friend request does not exist:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Create a friend request with sender=user and receiver=receiver.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Save the friend request in the database.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;iii. Response = ‘Friend request sent’  
> 3. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. User must be authenticated to send a friend request.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Response = ‘User must be authenticated’  
> 4. Send a HttpResponse of a json object with Responce as the data that will passed into the sendFriendRequest() ajax function.  
> 5. sendFriendRequest() ajax function will send the request to the receiver in the frontend and update the view.
  
  
## Accept Friend Request  

accepting a friend request made to a particular user.  
  
### Algorithm: accept_friend_request(request, *args, **kwargs)


> 1. Get the current user (i.e request.user).  
> 2. If the request method is GET and current user is authenticated:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Get ‘friend_request_id’ from kwargs.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Obtain friend-request-id of the friend request from the FriendRequest table using friend_request_id.  
> &nbsp;&nbsp;&nbsp;&nbsp;c. If friend-request-id.receiver == current user:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Call FriendRequest.accept() from the friend models which adds the friend (sender) to the user’s friend list.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Response = ‘Friend request accepted’  
> &nbsp;&nbsp;&nbsp;&nbsp;d. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. User (owner) cannot accept friend request which is sent to other users.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Response = ‘not your request to accept’  
> 3. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. User must be authenticated to accept a friend request.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Response = ‘User must be authenticated’  
> 4. Send a HttpResponse of a json object with Responce as the data that will passed into the acceptFriendRequest() ajax function.  
> 5. acceptFriendRequest() ajax function will accept the request made to the user in the frontend and update the view.
  
  

## Cancel Friend Request  
cancelling a friend request to a friend made by the user.  
  
  ### Algorithm: cancel_friend_request(request, *args, **kwargs)

> 1. Get the current user (i.e request.user).  
> 2. If the method is POST and current user is authenticated:   
> &nbsp;&nbsp;&nbsp;&nbsp;a. Get the ‘receiver_user_id’ from POST request  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Obtain receiver of the friend request from the AUTH_USER_MODEL using receiver_user_id.  
> &nbsp;&nbsp;&nbsp;&nbsp;c. Get the active friend request made by current user to receiver from FriendRequest table in the database.  
> &nbsp;&nbsp;&nbsp;&nbsp;d. If friend request exists:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Call FriendRequest.cancel() from the friend models which removes/deletes the request from the database.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Response = ‘Friend request cancelled’  
> &nbsp;&nbsp;&nbsp;&nbsp;e. Else if friend request does not exists:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Response = ‘Friend request does not exists’  
> 3. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. User must be authenticated to cancel a friend request.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Response = ‘User must be authenticated’  
> 4. Send a HttpResponse of a json object with Responce as the data that will passed into the cancelFriendRequest() ajax function.  
> 5. cancelFriendRequest() ajax function will cancel the request made to other user by current user in the frontend and update the view.

  
  
## Decline Friend Request  
declining a friend request made by another user to the owner.
  
  ### Algorithm: decline_friend_request(request, *args, **kwargs)

> 1. Get the current user (i.e request.user).  
> 2. If the request method is GET and current user is authenticated:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Get ‘friend_request_id’ from kwargs.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Obtain friend-request-id of the friend request from the FriendRequest table using friend_request_id.  
> &nbsp;&nbsp;&nbsp;&nbsp;c. If friend-request-id.receiver == current user:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Call FriendRequest.decline() from the friend models which rejects (sets is_active to False) the friend request made by other user to the current user.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Response = ‘Friend request declined’  
> &nbsp;&nbsp;&nbsp;&nbsp;d. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. User (owner) cannot decline friend request which is sent to other users.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Response = ‘not your request to decline’  
> 3. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. User must be authenticated to decline a friend request.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Response = ‘User must be authenticated’  
> 4. Send a HttpResponse of a json object with Responce as the data that will passed into the declineFriendRequest() ajax function.  
> 5. declineFriendRequest() ajax function will reject the request made to the current user by foreign user in the frontend and update the view.

  
  
## Removing a Friend  
unfollow/unfriending a friend from your friends list
  
  ### Algorithm: remove_friend(request, *args, **kwargs)

> 1. Get the current user (i.e request.user).  
> 2. If the method is POST and current user is authenticated:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Get the ‘receiver_user_id’ from POST request  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Obtain removee from the AUTH_USER_MODEL using receiver_user_id.  
> &nbsp;&nbsp;&nbsp;&nbsp;c. Get the friend list of the current user from FriendList table in the database.  
> &nbsp;&nbsp;&nbsp;&nbsp;d. If removee in friend list:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Call FriendList.unfriend(removee) from the friend models which removes the removee from current user’s friend list as well as removes the current user from the removee’s friend list.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Response = ‘Successfully removed that friend.’  
> &nbsp;&nbsp;&nbsp;&nbsp;e. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;i. Response = ‘removee is not your friend to remove’  
> 3. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. User must be authenticated to remove a friend.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Response = ‘User must be authenticated’  
> 4. Send a HttpResponse of a json object with Responce as the data that will passed into the removeFriend() ajax function.  
> 5. removeFriend() ajax function will remove the friend from the current user and removee’s friend list tab in the frontend and update the view.

  
  
## Friend Requests View  
view for viewing all the friend requests of the user
  
  ### Algorithm: friend_requests(request, *args, **kwargs)

> 1. Get the current user (i.e request.user)  
> 2. If current user is authenticated:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Get ‘user_id’ from kwargs.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Obtain user_account from the AUTH_USER_MODEL using user_id, which is the user whose friend request list is to be viewed   
> &nbsp;&nbsp;&nbsp;&nbsp;c. If user_account == current user:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Get all the active friend request of the user_account from FriendRequest table in the database.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Store it in context dictionary for the key ‘friend_requests’.  
> &nbsp;&nbsp;&nbsp;&nbsp;d. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Return HttpResponse("You can't view another users friend requets.")  
> 3. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Redirect to login page.  
> 4. Render the context to "friend/friend_requests.html".

  
  
## Friends List View  
listing all the friends of a particular user and also show whether you are friends with any of the friends in that user's friends list.
  
  ### Algorithm: friends_list_view(request, *args, **kwargs)

> 1. Get the current user (i.e request.user)  
> 2. If current user is authenticated:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Get ‘user_id’ from kwargs.  
> &nbsp;&nbsp;&nbsp;&nbsp;b. Obtain this_user from the AUTH_USER_MODEL using user_id, which is the user whose friend list is to be viewed   
> &nbsp;&nbsp;&nbsp;&nbsp;c. Get the friend list of this_user from FriendList table in the database.  
> &nbsp;&nbsp;&nbsp;&nbsp;d. If friend list does not exists or < 0:  
> &nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbspi. Return HttpResponse("Could not find friends list for this_user.”)  
> &nbsp;&nbsp;&nbsp;&nbsp;e. if user != this_user:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. if not user in friend_list.friends.all():  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Return HttpResponse("You must be friends to view their friends list." )  
> &nbsp;&nbsp;&nbsp;&nbsp;f. get the authenticated users friend list i.e the current user’s friend list.  
> &nbsp;&nbsp;&nbsp;&nbsp;e. For friend in friend list of this_user:  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i. Check if friend is a mutual friend of current user using FriendList.is_mutual_friend() from the friend models, which returns a boolean.  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii. Append (friend, boolean result) to a list  
> &nbsp;&nbsp;&nbsp;&nbsp;h. Store the list in the context dictionary for the key ‘friends’.  
> 3. Else:  
> &nbsp;&nbsp;&nbsp;&nbsp;a. Return HttpResponse("You must be friends to view their friends list.")  
> 4. Render the context to "friend/friend_list.html".

