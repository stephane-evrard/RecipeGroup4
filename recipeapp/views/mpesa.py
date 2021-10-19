# from django.http import HttpResponse, JsonResponse
# import requests
# from requests.auth import HTTPBasicAuth
# import json
# from django.views.decorators.csrf import csrf_exempt
# from recipeapp.models.models import MpesaPayment
# # from recipeapp.mpesa_credentials import LipanaMpesaPpassword, MpesaAccessToken


# def getAccessToken(request):
#     consumer_key = '9Ct0gNXcCKbcNBbX4IlMqO5lIChMsXiO'
#     consumer_secret = '9lthLw1bOfNAjt6I'
#     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

#     r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']

#     return HttpResponse(validated_mpesa_access_token)


# def lipa_na_mpesa_online(request):
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     request = {
#         "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
#         "Password": LipanaMpesaPpassword.decode_password,
#         "Timestamp": LipanaMpesaPpassword.lipa_time,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": 1,
#         "PartyA": 254794163715,  # replace with your phone number to get stk push
#         "PartyB": LipanaMpesaPpassword.Business_short_code,
#         "PhoneNumber":  254794163715,  # replace with your phone number to get stk push
#         "CallBackURL": "https://f4df-197-156-137-181.ngrok.io/con",
#         "AccountReference": "Mwashe",
#         "TransactionDesc": "Testing stk push"
#     }
    
    
    
#     response = requests.post(api_url, json=request, headers=headers)
#     print(request)
#     return HttpResponse(response)

# @csrf_exempt
# def call_back(request):
#     print(request)
#     return HttpResponse(request)

