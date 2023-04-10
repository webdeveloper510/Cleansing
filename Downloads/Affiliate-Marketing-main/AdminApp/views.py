from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from AdminApp.models import *
from AdminApp.serializer import *
from rest_framework.authtoken.models import Token
from CampaignApp.models import *
from CampaignApp.serializer import *
from rest_framework.authentication import TokenAuthentication

from AdminApp.permission import *

# Create your views here.

#Login API
class Login(APIView): 
    def post(self, request):
        username = request.data.get('email') 
        password = request.data.get('password')
        user = authenticate(username=username, password=password)   
        if user:
            login(request, user)
            print("user",user)
            refresh=Token.objects.create(user=user)
            return Response({'Success':"Login Successfully",'Token':str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdate(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    def put(self,request,pk):
        try:
            influencer = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateUserSerializer(influencer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


        
# Influencer api get , create,update ,delete
class InfluencerViewSet(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    
    def list(self, request):
        infu_list=User.objects.filter(user_type =2)
        serializer = UserSerializer(infu_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

    def create(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_type =2)
            return Response({"Success": "Influencer Created Successfully."},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            influencer = User.objects.get(pk = pk,user_type=2)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateUserSerializer(influencer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        influencer= User.objects.get(pk=pk,user_type=2)
        influencer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#List of Campaign api
class CampaignView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    def get(self,request):   
        campaign_list=Campaign.objects.all()
        serializer = CampaignSerializer(campaign_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)


#List of Campaign api get,create,update,delete
class CampaignViewSet(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsSuperuser]
    def list(self, request):
        campaign_list=Campaign.objects.all()
        serializer = CampaignSerializer(campaign_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

    def create(self, request):
        serializer=CampaignSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success":"Campaign create successfully","product_details":serializer.data},status=status.HTTP_200_OK)
        
        return Response({"error":"Campaign not created"},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            campaign_get = Campaign.objects.get(pk = pk)
            print(campaign_get)
        except Campaign.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateCampaignSerializer(campaign_get,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        camp_del=Campaign.objects.filter(id=pk)
        camp_del.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





#Logout api
class LogoutView(APIView):
    permission_classes = [IsSuperuser]
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=204)
   