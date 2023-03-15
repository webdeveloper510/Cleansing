from rest_framework.views import APIView
from rest_framework.response import Response
from restapp.models import *
from restapp.serializers import *
import requests
from rest_framework import generics, status
import json


headers={"Authorization": "Bearer yGrFqiK4YqDtqODbGRZkZrWRIgsjFLZP"}

class YoutubeFollower(APIView):
    def get(self,request):
        base_url="https://api.modash.io/v1/youtube/profile/@MortaLyt/report"
        response = requests.get(base_url, headers=headers)
        return Response({"success":json.loads(response.text)},status=status.HTTP_200_OK)
        
        
