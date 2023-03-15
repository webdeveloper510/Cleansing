from restapp.serializers import *
from restapp.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Register(APIView):
        def post(self,request):
            serializer=UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        
                return Response({"Success": "USER CREATED"},status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
           




    