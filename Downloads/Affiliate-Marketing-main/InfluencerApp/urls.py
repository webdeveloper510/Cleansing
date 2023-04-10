from django.urls import path
from InfluencerApp.views import *


urlpatterns = [
    
    #LOGIN/REGISTER URLS
    path("influencer/create/",Register.as_view(),name="influencer_register"),
    path("influencer/details/",Details.as_view(),name="details"),
    path("influencer/login/",InfluencerLogin.as_view(),name="influencer_login"),
    
    #INFLUENCER SHOW/EDIT/Logout URLS
    path('influencer/list/', InfluencerList.as_view(),name="Influencer-list"),
    path("influencer/update/<int:pk>/",UpdateInfluencer.as_view(),name="UpdateInfluencer"),  
    path('influencer/logout/', LogoutView.as_view(), name='logout'),
    
    
    #MODASH API URLS
    path('youtuber/',YoutubeFollower.as_view(),name="youtuber"),
    path('instagram/',InstagramFollower.as_view(),name="instagram"),
    
    
    #INFLUENCER CAMPAGIN APIS URLS
    path('influencer/accept/<int:id>/', AcceptView.as_view(), name='accept'),
    path('influencer/decline/<int:id>/', DeclineView.as_view(), name='decline'),
    path('influencer/campaign/', PendingCampaing.as_view(), name='campaign'),
 
]   