from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from CampaignApp.models import *
from CampaignApp.serializer import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import  status
from InfluencerApp.serializer import *
from Affilate_Marketing.settings import SHOPIFY_PRODUCT
import requests
import json
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from StoreApp.models import *
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your views here.

#To get access token
def access_token(self,request):
    user_obj=User.objects.filter(id=self.request.user.id)
    shop=user_obj.values("shopify_url")[0]["shopify_url"]
    acc_tok=Store.objects.filter(store_name=shop).values("access_token")[0]["access_token"]
  
    return acc_tok,shop
    


#REGISTER INFLUENCER API
class Register(APIView):
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_type =3)
            infl_id=serializer.data["id"]
            request.session["id"]=infl_id
            return Response({"Success": "Vendor Register Successfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
#LOGIN INFLUENCER API  
class VendorLogin(APIView): 
    def post(self, request):
            shop_url=request.data.get('shop')
            if shop_url:
                user_objects=User.objects.filter(shopify_url=shop_url).values("email","password")
                if user_objects:
                    user_obj=User.objects.filter(email=user_objects[0]["email"],password=user_objects[0]["password"])

                    email1=user_objects[0]["email"]
                    token_id=user_obj.values_list("id",flat=True)[0]
                
                    user_base = get_user_model()
                    usr_ins=user_base.objects.get(email=email1)
                    shop2=Store.objects.filter(store_name=shop_url)
            
                    if user_obj:
                        usr=Token.objects.filter(user_id=token_id)
                        if not usr:
                            token = Token.objects.create(user=usr_ins)
                            return Response({'Success':"Login Successfully",'Token':str(token),"shop_url":usr_ins.shopify_url}, status=status.HTTP_200_OK)
                           
                        else:
                            user_key=Token.objects.filter(user_id=token_id).values_list("key",flat=True)[0]
                            if shop2:
                                return Response({'Success':"Login Successfully",'Token':str(user_key),"shop_url":usr_ins.shopify_url,"admin_dahboard":"https://admin.shopify.com/store/marketplacee-app/apps/marketplace-49"}, status=status.HTTP_200_OK)
                            return Response({'Success':"Login Successfully",'Token':str(user_key),"shop_url":usr_ins.shopify_url}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Shop url not found'}, status=status.HTTP_400_BAD_REQUEST)
 
            else:
                email = request.data.get('email')    
                password = request.data.get('password')
                user=authenticate(username=email, password=password)
                if user:
                    login(request, user)
                    usr=Token.objects.filter(user_id=user.id)
                    if not usr:
                        refresh=Token.objects.create(user=user) 
                        return Response({'Success':"Login Successfully",'Token':str(refresh),"shop_url":user.shopify_url}, status=status.HTTP_200_OK)
                    else:
                       
                        user_token=Token.objects.filter(user_id=user.id).values_list("key",flat=True)[0]
                        shop2=User.objects.filter(id=user.id).values_list("shopify_url",flat=True)[0]
                        shop4=Store.objects.filter(store_name=shop2)
                        if shop4:
                            return Response({'Success':"Login Successfully",'Token':str(user_token),"shop_url":user.shopify_url,"admin_dahboard":"https://admin.shopify.com/store/marketplacee-app/apps/marketplace-49"}, status=status.HTTP_200_OK)
                        return Response({'Success':"Login Successfully",'Token':str(user_token),"shop_url":user.shopify_url}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
       
            


#API TO CREATE CAMPAIGN
class CreateCampaign(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    def post(self,request):
        serializer=CampaignSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(status=1,vendorid_id=self.request.user.id)
            return Response({"success":"Campaign create successfully","product_details":serializer.data},status=status.HTTP_200_OK)
        
        return Response({"error":"Campaign not created"},status=status.HTTP_400_BAD_REQUEST)


# API TO update CAMPAIGN 
class UpdateCampaign(APIView):
    def put(self,request,pk=None):
        try:
            campaign_get = Campaign.objects.get(Q(pk = pk,status=1)|Q(pk=pk,status=2)) 
           
        except Campaign.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
       
        serializer=CampaignUpdateSerializer(campaign_get,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    
#API TO CREATE INFLUENCER CAMPAIGN
class InfluencerCampaign(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    def post(self,request):
        serializer=InflCampSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(status=2,vendorid_id=self.request.user.id)
            return Response({"success":"Campaign create successfully","product_details":serializer.data},status=status.HTTP_200_OK)
        return Response({"error":"Campaign not created"},status=status.HTTP_400_BAD_REQUEST)

    

# API TO GET LIST OF CAMPAIGN   
class  PendingList(APIView):
    def get(self,request):
        campaign_obj=Campaign.objects.filter(campaign_status=0,vendorid_id=self.request.user.id)
        serializer=CampaignSerializer(campaign_obj,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    
    
# API TO GET LIST OF ACTIVE CAMPAIGN    
class  ActiveList(APIView):
    def get(self,request):
        campaign_obj=Campaign.objects.filter(campaign_status=1,vendorid_id=self.request.user.id)
        serializer=CampaignSerializer(campaign_obj,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)    
    

#API TO GET INFLUENCER CAMPAIGN LIST
class InflCampaignList(APIView):
    def get(self,request):
        campaign_obj=Campaign.objects.filter(status=2)

        serializer=CampaignSerializer(campaign_obj,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
     



#API TO DELETE A CAMPAIGN
class DeleteCampaign(APIView): 
    def delete(self, request, id):
            camp_del=Campaign.objects.filter(id=id)
            camp_del.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
#API TO GET INFLUENCER LIST
class InfluencerList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    def get(self,request):   
        infu_list=User.objects.filter(user_type =2)
        serializer = InfluencerSerializer(infu_list,many=True)
        handle=serializer.data[0]["username"]
        print(handle)
        # print("--------------",(serializer.data["username"]))
        headers={"Authorization": "Bearer jrleR5uSaSjc38OIMQu3iCjYGPZzwEmX"}
        base_url=f"https://api.modash.io/v1/instagram/profile/{handle}/report"
        response = requests.get(base_url, headers=headers)
        print(json.loads(response.text))
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    

# API TO GET Product list
class ProductList(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]   
    def get(self,request):
        acc_tok=access_token(self,request)
        headers= {"X-Shopify-Access-Token": acc_tok[0]}
        url=f"https://{acc_tok[1]}/admin/api/2023-01/products.json?status=active"
        response = requests.get(url, headers=headers)
        return Response({"success":json.loads(response.text)})    


#API TO GET STORED TOKEN
class GetToken(APIView):
    def post(self,request):
        shop_name=request.data.get("shop_name")
        if not shop_name:
                return Response({'error': 'Missing shop parameter'}, status=400)
        user=User.objects.filter(shopify_url=shop_name).values_list("id",flat=True)
        if user:
            usr_obj=user[0]
            token_obj=Token.objects.filter(user_id=usr_obj).values_list("key",flat=True)[0]
            return Response({"success":"hello","user_token":token_obj})
        else:
            return Response({'error': 'user not found'}, status=400)
        
        
    
    
#API TO GET CAMPAIGN COUNT
class CountCampaign(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated] 
    
    def get(self,request):
        active=Campaign.objects.filter(vendorid_id=self.request.user.id,campaign_status=1).count()
        pending=Campaign.objects.filter(vendorid_id=self.request.user.id,campaign_status=0).count()
        total=Campaign.objects.filter(vendorid_id=self.request.user.id).count()
        return Response({"active_campaign":active,"pending_campaign":pending,"total":total},status=status.HTTP_200_OK)
    
    
    
    
# API TO GET PRODUCT URL
class ProductUrl(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self,request):
        product_name=request.query_params.get('id')
        acc_tok=access_token(self,request)
        headers= {"X-Shopify-Access-Token": acc_tok[0]}
        
        response = requests.get(f"https://{acc_tok[1]}/admin/api/2023-01/products.json?id=" + product_name, headers=headers)
        prd_handle=json.loads(response.text)['products'][0]["handle"]
        prd_id=json.loads(response.text)['products'][0]["id"]
        print(prd_id)
        print(self.request.user.id)
        prod_obj=Productdetails()
        prod_obj.product_id=prd_id
        vendorid_id=self.request.user.id
        prod_obj.save()
        
        prod_des=json.loads(response.text)['products'][0]["body_html"]
        return Response({"URL":SHOPIFY_PRODUCT+str(prd_handle),"description":prod_des})

#API TO SEND REQUEST
class RequestSents(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]  

    def post(self,request):
        serializer=InflCampSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(status=2,vendorid_id=self.request.user.id)
            infll=serializer.data["influencer_name"]
            infll_id=serializer.data["id"]
            print(infll_id)
            res = json.loads(infll)
            
            for i in res:
                req_obj=RequestSent()
                req_obj.vendorid_id=self.request.user.id
                req_obj.campaignid_id=infll_id
                req_obj.influencee=i
                req_obj.status=1
                req_obj.save()
            
    
            return Response({"success":"Campaign create successfully","product_details":serializer.data},status=status.HTTP_200_OK)
        return Response({"error":"Campaign not created"},status=status.HTTP_400_BAD_REQUEST)



        

