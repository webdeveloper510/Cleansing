from django.urls import path
from CampaignApp.views import *

urlpatterns = [
    path('vendor/register/',Register.as_view(),name="vendor"),
    path('vendor/login/',VendorLogin.as_view(),name="vendorlogin"),
    path('create/',CreateCampaign.as_view(),name="campaign"),
    path('inflcampaign/create/',InfluencerCampaign.as_view(),name="inflcampaign"),
    path('active/',ActiveList.as_view(),name="campaignlist"),
    path('pending/',PendingList.as_view(),name="pending"),
    path('infllist/',InflCampaignList.as_view(),name="inflcampaignlist"),
    path('delete/<int:id>/',DeleteCampaign.as_view(),name="deletecamp"),
    path('influencer/list/',InfluencerList.as_view(),name="influencer"),
    path('product/list/',ProductList.as_view(),name="productlist"),
    path('get/token/',GetToken.as_view(),name="token"),
    # path('webhook-handler/',WebhookHandler.as_view(),name="handler"),
    path('update/<int:pk>/',UpdateCampaign.as_view(),name="campaignupdate"),
    path('count/',CountCampaign.as_view(),name="count"),
    path('product/url/',ProductUrl.as_view(),name="url"),
    path('request/url/',RequestSents.as_view(),name="request"),

   
]