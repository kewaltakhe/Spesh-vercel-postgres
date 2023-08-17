from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhotoUploadForm, UserProfileForm
from .models import PhotoModel, CustomUser
from .models import Follow
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.http import HttpResponseForbidden

def index_page_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

@login_required
def homepage_view(request):
    logged_user = request.user
    following_user_ids = Follow.objects.filter(follower=logged_user).values_list('following', flat=True)
    feedpage_photos = PhotoModel.objects.filter(user__in =  following_user_ids).order_by('-created_at')
    suggested_users = CustomUser.objects.exclude(id__in=(list(following_user_ids)+[request.user.id]))
    return render(request, 'homepage.html',{'feedpage_photos':feedpage_photos,'suggested_users':suggested_users})

@login_required
def userprofile_view(request):
    login_user = request.user
    follower_user_ids = Follow.objects.filter(following=login_user).values_list('follower', flat=True)
    followers = CustomUser.objects.filter(id__in=follower_user_ids)

    following_user_ids = Follow.objects.filter(follower=login_user).values_list('following', flat=True)
    followings = CustomUser.objects.filter(id__in=following_user_ids)

    user_photos = PhotoModel.objects.filter(user=login_user)

    photo_count = user_photos.count()
    return render(request,'logged_in_pages/user_profile.html',{'current_user':login_user,'user_photos':user_photos,'photo_count':photo_count,
                                                               'followers':followers,'followings':followings
                                                               ,'followers_count':followers.count,'followings_count':followings.count})

@login_required
def editprofile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'logged_in_pages/edit_profile.html', context)

@login_required
def uploadphoto_view(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('profile')
            
    else:
        form = PhotoUploadForm()
    return render(request,'logged_in_pages/upload_photo.html',{'form':form})     

@login_required
def deletephoto_view(request,photo_id):
    photo = get_object_or_404(PhotoModel, id=photo_id)
    if request.method=='POST':
        # User has confirmed the deletion
        photo.delete()
        print('PHOTO DELETED -----------------------',photo.id,'   url:',photo.image.url)
        return redirect('profile')
    print('PHOTO NOT DELETED -----------------------')
    return redirect('profile')

@login_required
def othersprofile_view(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    user_photos = PhotoModel.objects.filter(user=user)
    follower_user_ids = Follow.objects.filter(following=user).values_list('follower', flat=True)
    followers = CustomUser.objects.filter(id__in=follower_user_ids)

    following_user_ids = Follow.objects.filter(follower=user).values_list('following', flat=True)
    followings = CustomUser.objects.filter(id__in=following_user_ids)

    user_photos = PhotoModel.objects.filter(user=user)
    photo_count = user_photos.count()
    followers_count = str(followers.count())
    followings_count = str(followings.count())
    try:
        follow_object = Follow.objects.get(follower=request.user, following=user)
        if follow_object !=None:
            already_followed = True
        else:
            already_followed = True
        print("\033[92m {}\033[00m" .format("Already Followed"))
    except Exception as msg:
        print("\033[92m {}\033[00m" .format(msg))
        already_followed = False
    return render(request,'logged_in_pages/others_profile.html',{'current_user':request.user,'otheruser':user,'user_photos':user_photos,'photo_count':photo_count,
                                                                 'followers':followers,'followings':followings
                                                               ,'followers_count':followers_count,'followings_count':followings_count
                                                               ,'already_followed':already_followed})

@login_required
def usersearch_view(request):
    if request.method == 'GET':
        searchterm = request.GET.get('searchterm')
        logged_user = request.user
        if searchterm:
            results = CustomUser.objects.filter(username__icontains=searchterm)
        else:
            results = None

        return render(request,'logged_in_pages/search_results.html',{'results':results,'logged_user':logged_user})
    

@login_required
def followsomeone_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        following_user = CustomUser.objects.get(id=user_id)
        follower_user = request.user
        try:
            follow_object = Follow.objects.get(follower=follower_user, following=following_user)
            raise Exception('Already Followed')
        except:
            Follow.objects.create(follower=follower_user, following=following_user)
        followers_count = str(Follow.objects.filter(following=following_user).count())
        return JsonResponse({'message': 'User followed successfully.','followers_count':followers_count})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@login_required
def unfollowsomeone_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        following_user = CustomUser.objects.get(id=user_id)
        follower_user = request.user
        try:
            follow_object = Follow.objects.get(follower=follower_user, following=following_user)
            follow_object.delete()
        except:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
        followers_count = str(Follow.objects.filter(following=following_user).count())
        return JsonResponse({'message': 'User unfollowed successfully.','followers_count':followers_count})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
@login_required
def delete_account_view(request):
    token = get_random_string(length=32)
    request.session['delete_account_token'] = token
    return redirect('delete_account_confirm', token=token)

@login_required
def delete_account_confirm_view(request,token):
    session_token = request.session.get('delete_account_token')
    if token == session_token:
        if request.method == 'POST':
            user = request.user

            print("\033[92m {}\033[00m" .format(user.username+"Account Deleted"))
            user.delete()

            return redirect('index')
        return render(request, 'logged_in_pages/delete_account_confirm.html')
    else:
        return HttpResponseForbidden("Access denied")


