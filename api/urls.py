from django.urls import path, include
from . import login_views, user_views, like_view, comment_view, follow

urlpatterns = [
    
    path('login/', login_views.login_user, name='login'),
    path('logout/', login_views.logout_user, name='logout'),  
    path('users/', user_views.createuser, name= "createuser"), 
    path('profile/',user_views.profile, name= "profile"),
    path('profile/tweet/',user_views.profiletweet, name= "profiletweet"),
    path('tweet/',user_views.tweet.as_view()),
    path('likes/',like_view.like.as_view()),
    path('comment/',comment_view.comments.as_view()),
    path('search/',user_views.search, name= "search"),
    path('follow/',follow.follow.as_view()),
]