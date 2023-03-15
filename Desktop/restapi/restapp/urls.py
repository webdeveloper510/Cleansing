from django.urls import path
from restapp.views.SignupView import *
from restapp.views.LoginView import *
from restapp.views.ShopifyView import *
from restapp.views.ProductView import *
from restapp.views.CouponView import *
from restapp.views.InfluencerView import *
from restapp.views.CampaignView import *
from restapp.views.ModashView import *


urlpatterns = [
 
  path("register",Register.as_view(),name="register"),
  path("login",Login.as_view(),name="login"),
  path("product",ProductList.as_view(),name="product"),
  path("createproduct",CreateProduct.as_view(),name="createproduct"),
  path("pricerule",CreateCoupon.as_view(),name="pricerule"),
  path("discount",DiscountCoupon.as_view(),name="discount"),
  path("coupon",CouponList.as_view(),name="coupon"),
  path('password-reset/', PasswordResetView.as_view(),name="password-reset"),
  path('reset-password/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(),name="reset-password"),
  path('Influencer-list/', InfluencerList.as_view(),name="Influencer-list"),
  path('campaign/',CreateCampaign.as_view(),name="campaign"),
  path('youtuber/',YoutubeFollower.as_view(),name="youtuber"),
]