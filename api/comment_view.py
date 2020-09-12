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
import json
from datetime import datetime
from django.utils import timezone
from .models import *
import math
import random
import pytz
import requests
import re
from django.forms.models import model_to_dict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import os
from django.contrib.auth import get_user_model
User = get_user_model()


class comments(APIView):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(comments, self).dispatch(request, *args, **kwargs)

    # @permission_classes((IsAuthenticated, ))
    def post(self, request):
        email = ""
        tweet_id = ""
        text = ""
        try:
            b = request.body                
            body_json = json.loads(b)
            tweet_id = body_json['tweet_id']
            email = body_json['email']
            text = body_json['text']
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})
        try:
            check_user = AuthUser.objects.filter(email=email).exists()
            if check_user:
                user_id = AuthUser.objects.get(email=email).id
                Comment.objects.create(user_id=user_id ,tweet_id=tweet_id,text=text)
                return JsonResponse({'status':'success','message':'Commented Successfully'})
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})

    def get(self, request):
        result = []
        try:
            tweet_id = request.GET.get('id')
        except:
            pass
        try:
            check_comment = Comment.objects.filter(tweet_id = tweet_id).exists()
            if check_comment:
                comments = Comment.objects.filter(tweet_id = tweet_id)
                for comment in comments:
                    ans={}
                    ans["id"] = comment.id
                    ans["user_id"] = comment.user_id
                    ans["tweet_id"] = comment.tweet_id
                    ans["text"] = comment.text
                    first = AuthUser.objects.get(id=comment.user_id).first_name
                    last = AuthUser.objects.get(id=comment.user_id).last_name
                    name = first +" "+last
                    ans["name"] = name
                    username =  AuthUser.objects.get(id=comment.user_id).username
                    ans["username"] = username
                    result.append(ans)
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})  
        try:
            result = sorted(result, key = lambda i: i["id"],reverse=False)
            return JsonResponse({'data':result}, safe=False)
        except:
            return JsonResponse({'status':'fail','message':'Something went wrong'})
       