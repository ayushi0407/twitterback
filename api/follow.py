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


class follow(APIView):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(follow, self).dispatch(request, *args, **kwargs)

    # @permission_classes((IsAuthenticated, ))
    def post(self, request):
        user_by = ""
        user_to = ""
        check_user_to = ""
        check_user_by = ""
        try:
            b = request.body                
            body_json = json.loads(b)
            user_by = body_json['user_by']
            user_to = body_json['user_to']
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})
        try:
            check_user_to = AuthUser.objects.get(email=user_to).id
            check_user_by = AuthUser.objects.get(email=user_by).id
            check_follow = Follower.objects.filter(user_to=check_user_to ,user_by=check_user_by).exists()
            
            if check_follow:
                Follower.objects.filter(user_to=check_user_to ,user_by=check_user_by).delete()
                return JsonResponse({'status':'success','message':'Unfollowed'})
            else:
                Follower.objects.create(user_to=check_user_to ,user_by=check_user_by)
                return JsonResponse({'status':'success','message':'followed'})
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})

       