from rest_framework import serializers
from ShopifyApp.models import *



class ShopifySerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupon
        fields="__all__"