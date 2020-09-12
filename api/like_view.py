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


class like(APIView):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(like, self).dispatch(request, *args, **kwargs)

    # @permission_classes((IsAuthenticated, ))
    def post(self, request):
        email = ""
        tweet_id = ""
        try:
            b = request.body                
            body_json = json.loads(b)
            tweet_id = body_json['tweet_id']
            email = body_json['email']
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})
        print(1)
        try:
            check_user = AuthUser.objects.filter(email=email).exists()
            if check_user:
                user_id = AuthUser.objects.get(email=email).id
                check_like = Likes.objects.filter(user_id=user_id ,tweet_id=tweet_id)
                if check_like:
                    Likes.objects.filter(user_id=user_id ,tweet_id=tweet_id).delete()
                    return JsonResponse({'status':'success','message':'Tweet unliked'})
                else:
                    Likes.objects.create(user_id=user_id ,tweet_id=tweet_id)
                    return JsonResponse({'status':'success','message':'Tweet liked'})
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})

       