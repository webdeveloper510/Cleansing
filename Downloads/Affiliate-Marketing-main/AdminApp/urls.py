from django.urls import path
from AdminApp.views import *


urlpatterns = [
    path("login/",Login.as_view(),name="login"),
    path('profile/update/<int:pk>/', ProfileUpdate.as_view(),name="profile_update"),

    # influencer api
    path("influencer/list/",InfluencerViewSet.as_view({'get': 'list'}),name="influencerview"),
    path("influencer/create/",InfluencerViewSet.as_view({'post': 'create'}),name="influencercreate"),
    path("influencer/edit/<int:pk>/",InfluencerViewSet.as_view({'put': 'update'}),name="InfluencerUpdate"),
    path("influencer/delete/<int:pk>/",InfluencerViewSet.as_view({'delete': 'destroy'}),name="InfluencerUpdate"),


    # Campaign api
    path("campaign/list/",CampaignViewSet.as_view({'get': 'list'}),name="influencer_view"),
    path('campaign/create/', CampaignViewSet.as_view({'post': 'create'}),name="campaign_create"),
    path('campaign/edit/<int:pk>/', CampaignViewSet.as_view({'put': 'update'}),name="campaign_update"),
    path('campaign/delete/<int:pk>/', CampaignViewSet.as_view({'delete': 'destroy'}),name="campaign_update"),



    path("logout/",LogoutView.as_view(),name="logout"),
]
