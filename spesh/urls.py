from django.urls import path
from .views import (homepage_view,index_page_view,userprofile_view,
                    editprofile_view,uploadphoto_view,deletephoto_view,
                    othersprofile_view,usersearch_view,followsomeone_view,
                    unfollowsomeone_view,delete_account_view,delete_account_confirm_view,
                    get_followers_view
                    )

urlpatterns = [
    path('',index_page_view,name='index'),
    path('home/',homepage_view,name='home'),
    path('profile/',userprofile_view,name='profile'),
    path('edit_profile/',editprofile_view,name='edit_profile'),
    path('upload_photo/',uploadphoto_view,name='upload_photo'),
    path('delete_photo/<int:photo_id>/', deletephoto_view, name='delete_photo'),
    path('profile/<int:user_id>/',othersprofile_view,name='other_profile'),
    path('get_followers/<int:user_id>/',get_followers_view,name='get_followers'),
    path('search_result/',usersearch_view,name='usersearch'),
    path('follow_someone/',followsomeone_view,name='follow_someone'),
    path('unfollow_someone/',unfollowsomeone_view,name='unfollow_someone'),
    path('delete_account/',delete_account_view,name='delete_account'),
    path('delete_account/confirm/<str:token>/',delete_account_confirm_view,name='delete_account_confirm')
]