from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
import requests
import requests
import json
from Affilate_Marketing.settings import base_url ,headers ,SHOPIFY_API_KEY,SHOPIFY_API_SECRET
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from AdminApp.models import *
from StoreApp.models import *
from ShopifyApp.models import *
from ShopifyApp.serializers import *
from CampaignApp.models import *

# Create your views here.

#FUNCTION TO GET ACCESS TOKEN
def access_token(self,request):
    user_obj=User.objects.filter(id=self.request.user.id)
    shop=user_obj.values("shopify_url")[0]["shopify_url"]
    acc_tok=Store.objects.filter(store_name=shop).values("access_token")[0]["access_token"]
    print(acc_tok)
    return acc_tok,shop
    
    
#API TO FET PRODUCT LIST    
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
    
    



#API TO GET ORDER LIST
class OrderList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self,request):
        acc_tok=access_token(self,request)
        headers= {"X-Shopify-Access-Token": acc_tok[0]}
        base_url=f"https://{acc_tok[1]}/admin/api/2023-01/orders.json?status=anyn"
        response = requests.get(base_url, headers=headers)
        return Response({"success":json.loads(response.text)},status=status.HTTP_200_OK)



#API TO CREATE DISCOUNT
class CreateDiscountCodeView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        acc_tok=access_token(self,request)
        headers= {"X-Shopify-Access-Token": acc_tok[0]}
        base_url = f'https://{acc_tok[1]}/admin/api/2023-01'
 
       
        discount = request.data.get('discount_code')
        discount_type=request.data.get("discount_type")
        amount=request.data.get("amount")
        
        data = {
          "price_rule": {
                "title": discount,
                "target_type": "line_item",
                "target_selection": "all",
                "allocation_method": "across",
                "value_type":discount_type ,
                "value": amount, 
                "customer_selection": "all",
                "once_per_customer": True, 
                'starts_at': '2023-04-06T00:00:00Z',
            }
        }

        response = requests.post(f"{base_url}/price_rules.json", headers=headers, json=data)
        price_id=json.loads(response.text)["price_rule"]["id"]
        discount_code(price_id,acc_tok[1],headers,discount)
        if response.ok:
            return Response({"message":"coupon created successfully","coupon": discount},status=status.HTTP_201_CREATED)
        else:
            return Response({"response":response},status=status.HTTP_400_BAD_REQUEST)
        
        
def discount_code(price_id,shop,headers,discount_code):
  
    discount_code_endpoint = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{shop}/admin/api/2023-01/price_rules/{price_id}/discount_codes.json'

    discount_code_data = {
        'discount_code': {
            'code': discount_code,
            'usage_limit': 1,
            'customer_selection': 'all',
            'starts_at': '2023-04-06T00:00:00Z',
            'ends_at': '2023-04-30T23:59:59Z'
        }
    }


    discount_code_response = requests.post(discount_code_endpoint, json=discount_code_data,headers=headers)
    
    

    if discount_code_response.status_code == 201:
        print('Discount code created successfully!')
    else:
        print(f'Error creating discount code: {discount_code_response.text}')
    
        

#API TO CREATE DISCOUNT
class DiscountCodeMultiple(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def post(self, request):
      
        acc_tok=access_token(self,request)
        headers= {"X-Shopify-Access-Token": acc_tok[0]}
        base_url = f'https://{acc_tok[1]}/admin/api/2023-01'
   
        discount = request.data.get('discount_code')
        discount_type=request.data.get("discount_type")
        amount=request.data.get("amount")
  
        data = {
          "price_rule": {
                "title": discount,
                "target_type": "line_item",
                "target_selection": "all",
                "allocation_method": "across",
                "value_type": discount_type,
                "value":amount,
                "customer_selection": "all",
                'starts_at': '2023-04-06T00:00:00Z',

            }
        }
        
        coup_obj=Coupon()
        coup_obj.vendorid_id=self.request.user.id
        coup_obj.coupon=discount_type
        coup_obj.save()
        
        response = requests.post(f"{base_url}/price_rules.json", headers=headers, json=data)
        price_id=json.loads(response.text)["price_rule"]["id"]
        discount_code(price_id,acc_tok[1],headers,discount)
        if response.ok:
            return Response({"coupon": discount},status=status.HTTP_201_CREATED)
        else:
            return Response({"response":response},status=status.HTTP_400_BAD_REQUEST)
        
        
def discount_code(price_id,shop,headers,discount_code):
  
    discount_code_endpoint = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{shop}/admin/api/2023-01/price_rules/{price_id}/discount_codes.json'

    # Set up the data for the discount code
    discount_code_data = {
        'discount_code': {
            'code': discount_code,
            'usage_limit': None,
            'customer_selection': 'all',
            'starts_at': '2023-04-06T00:00:00Z',
            'ends_at': '2023-04-30T23:59:59Z'
        }
    }

    
    discount_code_response = requests.post(discount_code_endpoint, json=discount_code_data,headers=headers)
    
    
    # Check if the discount code was created successfully
    if discount_code_response.status_code == 201:
        print('Discount code created successfully!')
    else:
        print(f'Error creating discount code: {discount_code_response.text}')
        





#API TO CREATE DISCOUNT
# class ParticularProduct(APIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes = [IsAuthenticated]  
#     def post(self, request):
      
#         acc_tok=access_token(self,request)
#         headers= {"X-Shopify-Access-Token": acc_tok[0]}
#         base_url = f'https://{acc_tok[1]}/admin/api/2023-01'
#         # Get the discount code from the request data
      
#         discount = request.data.get('discount_code')
#         product_name=request.data.get("product_name")
#         get_product_id(product_name,acc_tok[1],headers)
#         print(get_product_id(product_name,acc_tok[1],headers))
#         z=get_product_id(product_name,acc_tok[1],headers)
#         # Create the discount code in Shopify
#         data = {
#           "price_rule": {
#                 "title": discount,
#                 "target_type": "line_item",
#                 "target_selection": "all",
#                 "allocation_method": "across",
#                 "value_type": "fixed_amount",
#                 "value": "-10.0", # Change this to the value of your discount
#                 "customer_selection": "all",
#                 # "once_per_customer": True, # Limit the coupon to one use per customer
#                 'starts_at': '2023-04-06T00:00:00Z',
#                 'prerequisite_product_ids':z
#             }
#         }
        
#         response = requests.post(f"{base_url}/price_rules.json", headers=headers, json=data)
#         price_id=json.loads(response.text)["price_rule"]["id"]
#         discount_code(price_id,acc_tok[1],headers,discount)
#         if response.ok:
#             return Response({"coupon": discount},status=status.HTTP_201_CREATED)
#         else:
#             return Response({"response":response},status=status.HTTP_400_BAD_REQUEST)
        
        
# def get_product_id(product_name,shop_name,headers):

   
#     response = requests.get(f"https://{shop_name}/admin/api/2023-01/products.json?title=" + product_name, headers=headers)
#     prd_handle=json.loads(response.text)['products'][0]["handle"]
#     prd_id=json.loads(response.text)['products'][0]["id"]

#     return prd_id 
    
        
# #API for particular product
# def discount_code(price_id,shop,headers,discount_code):
    
  
#     discount_code_endpoint = f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{shop}/admin/api/2023-01/price_rules/{price_id}/discount_codes.json'

#     # Set up the data for the discount code
#     discount_code_data = {
#         'discount_code': {
#             'code': discount_code,
#             'usage_limit': None,
#             'customer_selection': 'all',
#             'starts_at': '2023-04-06T00:00:00Z',
#             'ends_at': '2023-04-30T23:59:59Z'
#         }
#     }

#     # Send the request to create the discount code
#     discount_code_response = requests.post(discount_code_endpoint, json=discount_code_data,headers=headers)
    
    
#     # Check if the discount code was created successfully
#     if discount_code_response.status_code == 201:
#         print('Discount code created successfully!')
#     else:
#         print(f'Error creating discount code: {discount_code_response.text}')
        


class DiscountCodeView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self, request, format=None):
        acc_tok=access_token(self,request)
        headers= {"X-Shopify-Access-Token": acc_tok[0]}
        url = 'https://marketplacee-app.myshopify.com/admin/api/2023-01/price_rules.json?status=active'
        

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            
            coupons = response.json()['price_rules']
            discount_list=[]
            for discount in coupons:    
                discount_data = {
                'title': discount['title'],
                'id': discount['id']
                }
                discount_list.append(discount_data)

           
    
            return Response({"coupon":coupons})
        else:
            return Response({'message': response.text}, status=response.status_code)


class EditCodeView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self, request, format=None):
        # acc_tok=access_token(self,request)
        
        # headers= {"X-Shopify-Access-Token": acc_tok[0]}
        headers= {"X-Shopify-Access-Token": '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'}
        url =f'https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@marketplacee-app.myshopify.com/admin/api/2023-01/price_rules/1378892218660.json'
        print(url)
        print("url is not there")
        print("hello")
        data=json.dumps(request.data)
        print(data)
        response = requests.put(url,headers=headers,data=data)

    # Check if the discount was successfully deleted and return a DRF response
        if response.status_code == 200:
            return Response({'message': 'Discount deleted successfully'})
        else:
            return Response({'message': response.text}, status=response.status_code)
        

      



        
    
        
class UninstallView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        # Retrieve the shop domain and access token from the request data
        shop_domain = request.data.get('shop_domain')
        user_obj=User.objects.filter(id=self.request.user.id)
        shop=user_obj.values("shopify_url")[0]["shopify_url"]
        acc_tok=Store.objects.filter(store_name=shop).values("access_token")[0]["access_token"]
        print(acc_tok)
        # Send a DELETE request to the app uninstall URL
        uninstall_url = f"https://{shop_domain}/admin/api/2021-07/applications/{acc_tok}.json"
        headers = {"Content-Type": "application/json"}
        response = requests.delete(uninstall_url, headers=headers)

        # Check if the app was uninstalled successfully
        if response.status_code == 200:
            return Response({'message': 'App uninstalled successfully'})
        else:
            return Response({'message': 'Failed to uninstall app'}, status=400)
        