
from rest_framework.views import APIView
from rest_framework.response import Response



# class shop(APIView):
#     def post(self,request):    
#         try:
#             # session1=shopify.Session("puma-1744.myshopify.com")
#             # print("==========",session1)
#             # shop=shopify.ShopifyResource.set_site("https://puma-1744.myshopify.com/")
#             # print("============",shop)
#             session=shopify.Session.setup(api_key="95e574f97f5e5829ec18351ee37e81d1", secret="adc3f900c1bfaca31a0a6b120a69249c")
#             print("------------",session)
#             shopify.ShopifyResource.activate_session(session)

#             # products = shopify.Product.find()
#             # print("---",products)
#             return Response({"success":"product"})
#         except Exception as e:
#             print("00000000",e)
#             return Response({"error":"product"})


# # import shopify



# # SHOPIFY_API_KEY = 'your_api_key'
# # SHOPIFY_API_PASSWORD = 'your_api_password'
# # SHOPIFY_STORE_NAME = 'your-shopify-store.myshopify.com'

# # # Authenticate with Shopify
# # session = shopify.Session(SHOPIFY_STORE_NAME, SHOPIFY_API_KEY, SHOPIFY_API_PASSWORD)
# # shopify.ShopifyResource.activate_session(session)

# # # Fetch products from the store
# # products = shopify.Product.find()

# # # Deactivate the Shopify session
# # shopify.ShopifyResource.clear_session()