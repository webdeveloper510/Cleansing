from rest_framework import serializers
from AdminApp.models import *
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from CampaignApp.models import *
from InfluencerApp.models import *



class InfluencerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True,required=True)
    

    def create(self, validated_data):
        
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        validated_data['password'] = make_password(password)       
        print(validated_data['password'])

        return super(InfluencerSerializer, self).create(validated_data) 
    
    
    class Meta:
        
        model=User
        fields=["id","username","email","password","user_type","confirm_password","country"]
        extra_kwargs = {
            'password': {'required': True},
            'confirm_password': {'required': True},
            'country': {'required': True},
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
       
 
class UpdateInfluencerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
   
   
    def update(self, instance, validated_data):
        password = validated_data.get('password',None)
        
        if password:
            instance.password = validated_data.get('password', instance.password)
            print("-------------------------------------",instance.password)
            validated_data['password'] = make_password(instance.password)   
        else:
            validated_data.pop('password', None)
  
        return super(UpdateInfluencerSerializer , self).update(instance,validated_data)
    
    
    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Influencer with this email already exists")
        return lower_email
    
    class Meta:
        
        model=User
        fields=["username","email","password"]
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
          
        }
    
    def validate_password(self,password):
        if len(password)< 8:
            raise serializers.ValidationError("Password must be more than 8 character.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one digit.')
        return password 
    
    
class StepTwoSerializer(serializers.ModelSerializer):
    class Meta:
        model=InfluencerDetails
        fields="__all__"
        extra_kwargs = {
            'industries': {'required': True},
            'experience': {'required': True},
            'promotion': {'required': True},
            'customer_age': {'required': True},
            'gender': {'required': True},
            'location': {'required': True}
          
        }
        
        
    

    
    
    
