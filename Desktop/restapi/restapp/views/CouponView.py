from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from restapi.settings import  headers
import json
from rest_framework import generics, status


#API TO CREATE PRICE RULE FOR COUPON CODE
class CreateCoupon(APIView):
    def post(self,request):
        base_url="https://puma-1744.myshopify.com/admin/api/2023-01/price_rules.json"
        price=request.data.get("price_rule")
        body={"price_rule":price}
        response = requests.post(base_url, headers=headers,json=body)
        return Response({"success":json.loads(response.text)},status=status.HTTP_200_OK)


#API TO CREATE COUPON CODE
class DiscountCoupon(APIView):
    def post(self,request):
        base_url="https://puma-1744.myshopify.com/admin/api/2023-01/price_rules/1382412353825/batch.json"
        coupon=request.data.get("discount_codes")
        body={"discount_codes":coupon}
        response = requests.post(base_url, headers=headers,json=body)
        return Response({"success":json.loads(response.text)},status=status.HTTP_200_OK)

#API TO GET COUPON LIST
class CouponList(APIView):
    def get(self,request):
        base_url="https://puma-1744.myshopify.com/admin/api/2023-01/price_rules/1382412353825/discount_codes.json"
        response = requests.get(base_url, headers=headers)
        return Response({"success":json.loads(response.text)},status=status.HTTP_200_OK)


