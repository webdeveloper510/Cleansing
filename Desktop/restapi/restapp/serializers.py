from rest_framework import serializers
from restapp.models import *
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        print(password)
        validated_data['password'] = make_password(password)       
     
        return super(UserSerializer, self).create(validated_data) 
    
    
    class Meta:
        
        model=User
        fields=["username","email","password","country"]
        extra_kwargs = {
            'password': {'required': True},
            'username': {'required': True}
        }
    
    def validate_password(self,password):
        if len(password)< 8:
            raise serializers.ValidationError("Password must be more than 8 character.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one digit.')
        return password
    
    def validate_country(self,country):
        if country.isalpha() == False:
            raise serializers.ValidationError("Country must be in string")
        return country
    
    
        
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        if len(data.get('password'))< 8:
            raise serializers.ValidationError("Password must be more than 8 character.")
        if not any(char.isdigit() for char in data.get('password')):
            raise serializers.ValidationError('Password must contain at least one digit.')
        return data
      
    

 
class InfluencerSerializer(serializers.ModelSerializer):
   class Meta:
    model=User
    fields = ['username', 'email',"country"]
 
 

 
class CampaignSerializer(serializers.ModelSerializer):
   product_name=serializers.ListField()
   influencer_name=serializers.ListField()
   
   class Meta:
        model=Campaign
        fields = ['product_name', 'campaign_name',"influencer_name","coupon"]
        extra_kwargs = {
                'product_name': {'required': True},
                'campaign_name': {'required': True},
                'influencer_name': {'required': True},
                'coupon': {'required': True}
            }
