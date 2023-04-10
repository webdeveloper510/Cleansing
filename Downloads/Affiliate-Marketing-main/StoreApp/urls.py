from django.urls import path
from StoreApp.views import *

urlpatterns = [
      
  #INSTALL/AUTHORIZE APP URLS
  path('install/', InstallView.as_view(), name='install'),
  path('callback/', CallbackView.as_view(), name='shopify_callback'),
  path('details/', StoreDetails.as_view(), name='details'),
  # path('check/', CheckStore.as_view(), name='check'),
    
]