from rest_framework.views import APIView
from rest_framework.response import Response
from restapp.models import *
from restapp.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status



class InfluencerList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self,request):   
        infu_list=User.objects.all()
        serializer = InfluencerSerializer(infu_list,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
        
        