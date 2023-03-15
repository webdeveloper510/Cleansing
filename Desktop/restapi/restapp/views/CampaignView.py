from rest_framework.views import APIView
from rest_framework.response import Response
from restapp.models import *
from restapp.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status


#API TO CREATE CAMPAIGN
class CreateCampaign(APIView):
    def post(self,request):
        serializer=CampaignSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # print("------------",serializer.data)
            serializer.save()
            return Response({"success":"Campaign create successfully","product_details":serializer.data},status=status.HTTP_200_OK)
        
        return Response({"error":"Campaign not created"},status=status.HTTP_400_BAD_REQUEST)
    
    