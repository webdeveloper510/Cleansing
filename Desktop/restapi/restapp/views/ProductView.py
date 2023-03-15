from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import json
from restapi.settings import base_url , headers



# API TO GET PRODUCT LIST
class ProductList(APIView):
    def get(self,request):
        response = requests.get(base_url, headers=headers)
        return Response({"success":json.loads(response.text)})


# API TO CREATE A PRODUCT
class CreateProduct(APIView):
    def post(self,request):
        title=request.data.get("product")
        body = {"product":title}
        response = requests.post(base_url,headers=headers,json=body)
        return Response({"success":json.loads(response.text)})


