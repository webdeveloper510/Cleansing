from django.urls import path
from ShopifyApp.views import *

urlpatterns = [

  
  #SHOPIFY APPS URLS
  path("createproduct",CreateProduct.as_view(),name="createproduct"),
  path("product/list",CreateProduct.as_view(),name="product/list"),
  path("order",OrderList.as_view(),name="order"),
  path("discountcode/",CreateDiscountCodeView.as_view(),name="discountcode"),
  # path("paricular/",ParticularProduct.as_view(),name="paricular"),
  path("multiple/",DiscountCodeMultiple.as_view(),name="multiple"),
  path("coupon/list/",DiscountCodeView.as_view(),name="couponlist"),
  path('uninstall/', UninstallView.as_view(), name='uninstall'),
  path('delete/', EditCodeView.as_view(), name='delete'),
  
]