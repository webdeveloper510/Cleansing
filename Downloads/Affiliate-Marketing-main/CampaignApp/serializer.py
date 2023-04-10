from rest_framework import serializers
from CampaignApp.models import *
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True,required=True)
    

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        validated_data['password'] = make_password(password)       
        print(validated_data['password'])
        return super(RegisterSerializer, self).create(validated_data) 
    
    
    class Meta:
        
        model=User
        fields=["id","username","email","password","user_type","confirm_password","shopify_url","instagram_url","category"]
        extra_kwargs = {
            'password': {'required': True},
            'email': {'required': True},
            'confirm_password': {'required': True},
            'shopify_url': {'required': True},
            'instagram_url': {'required': True},
            'category': {'required': True},
            'username': {'required': True}
        }
    
    def validate_password(self,password):
        
                # if password != confirm_password:
                #     raise serializers.ValidationError('Password must match')
            if len(password)< 8:
                raise serializers.ValidationError("Password must be more than 8 character.")
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError('Password must contain at least one digit.')
            return password
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Password fields did not match.")
        return attrs
   
    def validate_shopify_url(self,shopify_url):
        if "//" in shopify_url or "/" in shopify_url:
            raise serializers.ValidationError("Please enter url name")
        
        if shopify_url == "":
            raise serializers.ValidationError("Shopify_url cannot be empty")
            
        return shopify_url


    def validate_instagram_url(self,instagram_url):

        if instagram_url == "":
            raise serializers.ValidationError("instagram_url cannot be empty")
            
        return instagram_url
    
    
class CommaSeparatedField(serializers.CharField):
    def to_internal_value(self, data):
        if not data:
            return []
        data_list=data.split(",")
        int_list = [int(num) for num in data_list]

        return int_list

class CampaignSerializer(serializers.ModelSerializer):
   product= CommaSeparatedField()
  
   class Meta:
        model=Campaign
        fields = ['id','campaign_name',"offer","product_discount","product","date","description","influencer_visit","coupon"]
        extra_kwargs = {
                'campaign_name': {'required': True},
                'date': {'required': True},
                #'influencer_name': {'required': True},
                'offer': {'required': True},
                'product': {'required': True},
                'product_discount': {'required': True},
            
            }


class InflCampSerializer(serializers.ModelSerializer):
   influencer_name=CommaSeparatedField()
   product= CommaSeparatedField()
   class Meta:
        model=Campaign
        fields = ['id','product', 'campaign_name',"influencer_name","coupon","date","influencer_visit","offer","product_discount","description"]
        extra_kwargs = {
                'product': {'required': True},
                'campaign_name': {'required': True},
                'influencer_visit': {'required': False},
                'offer': {'required': False},
                'product_discount': {'required': False},
                'influencer_name': {'required': True},
                'date': {'required': False},
                'coupon': {'required': False}
            }



class CampaignUpdateSerializer(serializers.ModelSerializer):
   class Meta:
        model=Campaign
        fields = ["id",'campaign_name','influencer_visit',"offer","product_discount","product","date","description","influencer_name"]  