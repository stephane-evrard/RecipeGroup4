import json
import logging
# from os import sync
from re import A
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import context
from recipeapp.forms.recipe import ReviewForm
from django.core.mail import send_mail
from recipeapp.models.models import Recipe, Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
def home(request):
    try:
        query = request.GET.get('q')
       
        recipes=Recipe.search(query)
        print(query)
        context={
            'recipe':recipes
        }
        
    except:
        recipe=Recipe.objects.all().order_by('created_at').reverse()
        
        context={
            'recipe':recipe
        }
 
    
    return render(request,'home/home.html',context)
def filter_recipes(request,what):
    recent=Recipe.filter_by_recent()
    ratings=Recipe.filter_by_rating()
    country=Recipe.filter_by_country()
    all=Recipe.objects.all().order_by('created_at').reverse()
    if what=='recent':
         context={
            'recipe':recent
        }
    elif what=='ratings':
        context={
            'recipe':ratings
        }
    elif what=='country':
        context={
            'recipe':country
        }
    else:
        context={
            'recipe':all
        }
    return render(request ,'home/home.html',context)


 
       
   
    
    return render(request,'home/home.html',context)


def viewpage(request,recipe_id):
    """
    Displays a detailed view of the recipes as specified in the URL.
    """
    user = request.user
    form=ReviewForm()
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = recipe.ingredient_set.order_by('-index')
    directions = recipe.direction_set.order_by('-index')
    comments=Review.objects.filter(recipe=recipe_id)
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'directions': directions,
        'form':form,
        'comments':comments
        
    }
    return render(request,'core/rec_details.html',context)
@login_required()
def user_dashboard(request):
    return render(request, 'home/dashboard.html')

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://91563395.ngrok.io/api/v1/c2b/confirmation",
               "ValidationURL": "https://91563395.ngrok.io/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

@csrf_exempt
def call_back(request):
    data=request.GET.get('body')
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    print(mpesa_payment)
    print(data)
    # payment = MpesaPayment(
    #     first_name=mpesa_payment['FirstName'],
    #     last_name=mpesa_payment['LastName'],
    #     middle_name=mpesa_payment['MiddleName'],
    #     description=mpesa_payment['TransID'],
    #     phone_number=mpesa_payment['MSISDN'],
    #     amount=mpesa_payment['TransAmount'],
    #     reference=mpesa_payment['BillRefNumber'],
    #     organization_balance=mpesa_payment['OrgAccountBalance'],
    #     type=mpesa_payment['TransactionType'],

    # )
    # payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return  HttpResponse(context)
    # return JsonResponse(dict(context))