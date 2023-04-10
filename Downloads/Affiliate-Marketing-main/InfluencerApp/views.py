from InfluencerApp.serializer import *
from InfluencerApp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from AdminApp.views import *
from CampaignApp.serializer import *
import requests
import json
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

    
headers={"Authorization": "Bearer yGrFqiK4YqDtqODbGRZkZrWRIgsjFLZP"}

#REGISTER INFLUENCER API
class Register(APIView):
    def post(self,request):
     
        serializer=InfluencerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_type =2)
            infl_id=serializer.data["id"]
            request.session["id"]=infl_id
            return Response({"Success": "Influencer Register Successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
            
class Details(APIView):
    def post(self,request):
        serializer=StepTwoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            serializer.save(influencerid_id=request.session["id"])
            return Response({"Success": "Next Step"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
#LOGIN INFLUENCER API  
class InfluencerLogin(APIView): 
    def post(self, request):
      
        username = request.data.get('email')
        print(username)
        password = request.data.get('password')
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            refresh=Token.objects.create(user=user)
            return Response({'Success':"Login Successfully",'Token':str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
        
            
           
           
#SHOW LIST OF INFLUENCER API
class InfluencerList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):   
        infu_list=User.objects.filter(user_type =2)
        serializer = InfluencerSerializer(infu_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    



#YOUTUBER FOLLOWER API
class YoutubeFollower(APIView):
    
    def get(self,request):
        user_handler=request.GET.get("user")
        base_url=f"https://api.modash.io/v1/youtube/profile/{user_handler}/report"
        response = requests.get(base_url, headers=headers)
        return Response({"success":json.loads(response.text)},status=status.HTTP_200_OK)
    
    
    
#INSTAGRAM FOLLOWER API
class InstagramFollower(APIView):
    def get(self,request):
        user_handler=request.GET.get("user")
        base_url=f"https://api.modash.io/v1/instagram/profile/{user_handler}/report"
        response = requests.get(base_url, headers=headers)
        return Response({"success":json.loads(response.text)},status=status.HTTP_200_OK)
    
    
#UPDATE INFLUENCER DATA API   
class UpdateInfluencer(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self,request,pk):
        try:
            influencer = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UpdateInfluencerSerializer(influencer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
#ACCEPT CAMPAIGN API
class AcceptView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    def post(self,request,id):
        try:
            cam_obj=Campaign.objects.filter(id=id).update(status=1,Influencerid_id=self.request.user.id)
            return Response({"message":"Campaign Accepted"},status=status.HTTP_200_OK)
        except:
            return Response({"error":"Issue in Campaign"},status=status.HTTP_400_BAD_REQUEST)
    
    
#DECLINE CAMPAIGN API
class DeclineView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    def post(self,request,id):
        try:
           
            cam_dec=Campaign.objects.filter(id=id).update(status=2,Influencerid_id=self.request.user.id)
            return Response({"message":"Campaign Decline"},status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


#LIST OF CAMPAIGN API
class PendingCampaing(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]    
    def get(self,request):   
        try:
            campaign_list=Campaign.objects.filter(status=0)
            serializer = CampaignSerializer(campaign_list,many=True)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
#LOGOUT API
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=204)