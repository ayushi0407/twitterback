from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.utils import timezone
from .models import *
import math
import random
import pytz
import requests
from .utils import *
from django.core.files.storage import FileSystemStorage
from xlrd import open_workbook
import xlrd
import string
from django.forms.models import model_to_dict
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()

#==================views=========================
@csrf_exempt
def login_user(request):    
    e = p = u =""
    try:
        b = request.body        
        body_json = json.loads(b)
        e = body_json['email']
        p = body_json['password']
        u = e.split('@')[0]
    except Exception as ex:
        return user_response('fail','Something went wrong',None,None,None,None,None)       
    check = AuthUser.objects.filter(email=e).exists()
    if check:
        user = authenticate(username=u, password=p)        
        if user:
            user_id = user.id            
            token, created = Token.objects.get_or_create(user_id=user_id)
            token_key = token.key
            return JsonResponse ({
                'status':'success',
                'message':'user logged in',
                'email':e,
                'token':token_key,
                'first_name':user.first_name, 
                'last_name':user.last_name,
            })
    return JsonResponse ({
                'status':'fail',
                'message':'Incorrect email or password'
            })

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def logout_user(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass
    logout(request)
    return JsonResponse({"status":"success", "message":"Successfully logged out"},status=200)














    

