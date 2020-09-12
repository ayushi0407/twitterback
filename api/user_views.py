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
from .user_utils import *
from django.contrib.auth import get_user_model
User = get_user_model()


@csrf_exempt
def createuser(request):
    f = l = e = ph = p =  ""
    try:
        b = request.body                
        body_json = json.loads(b) 
        f = body_json['firstname']
        l = body_json['lastname']
        e = body_json['email']    
        ph = body_json['phonenumber']
        p = body_json['password']
        for key in body_json:
            if body_json[key] == None:
                raise Exception("Missing values")
    except Exception as ex:
        return JsonResponse({'status':'fail','message':'Something went wrong'})
    return JsonResponse(signup_user(f,l,e,ph,p))


def profile(request):
    result = []
    tweetcount = 0
    follower = 0
    following = 0
    email = ""
    myemail = ""
    myuserid = ""
    try:
        email = request.GET.get('email')
        myemail = request.GET.get('myemail')
        myuserid = AuthUser.objects.get(email=myemail).id
    except:
        pass
    try:
        check_user = AuthUser.objects.filter(email=email).exists()
        res = {}
        if check_user:
            user = AuthUser.objects.get(email=email)
            res["id"] = user.id
            res["name"] = user.first_name + " " + user.last_name
            res["email"] = user.email
            res["username"] = user.username
            tweetcount = Tweets.objects.filter(user_id = user.id).count()
            res["tweetcount"] = tweetcount
            following = Follower.objects.filter(user_to = user.id).count()
            res["following"] = following
            follower = Follower.objects.filter(user_by = user.id).count()
            res["follower"] = follower
            check_follow = Follower.objects.filter(user_to=user.id ,user_by=myuserid).exists()
            if check_follow:
                res["follow"] = True
            else:
                res["follow"] = False
            result.append(res)
    except:
        pass
    return JsonResponse({'data':result}, safe=False)

def profiletweet(request):
    id_list = ""
    email = ""
    myemail = ""
    result = []
    myuserid = ""
    try:
        email = request.GET.get('email')
        myemail = request.GET.get('myemail')
        myuserid = AuthUser.objects.get(email=myemail).id
    except:
        pass
    try:
        check_user = AuthUser.objects.filter(email=email).exists()
        if check_user:
            user_id = AuthUser.objects.get(email=email).id
            tweets = Tweets.objects.filter(user_id=user_id)
            for tweet in tweets:
                ans = {}
                ans["id"] = tweet.id
                ans["user_id"] = tweet.user_id
                ans["text"] = tweet.text
                first = AuthUser.objects.get(id=tweet.user_id).first_name
                last = AuthUser.objects.get(id=tweet.user_id).last_name
                name = first +" "+last
                ans["name"] = name
                username =  AuthUser.objects.get(id=tweet.user_id).username
                ans["username"] = username
                likes = Likes.objects.filter(tweet_id = tweet.id).count()
                ans["likes"] = likes
                comment = Comment.objects.filter(tweet_id = tweet.id).count()
                ans["comment"] = comment
                check_like = Likes.objects.filter(tweet_id =tweet.id,user_id = myuserid).exists()
                if check_like:
                    ans["liked"] = True
                else:
                    ans["liked"] = False
                result.append(ans)
    except Exception as ex:
        return JsonResponse({'status':'fail','message':'Something went wrong'})  
    try:
        result = sorted(result, key = lambda i: i['id'],reverse=True) 
        return JsonResponse({'data':result}, safe=False)
    except:
        return JsonResponse({'status':'fail','message':'Something went wrong'})

def search(request):
    text = ""
    result = []
    try:
        text = request.GET.get('text')
    except:
        pass
    try:
        if text == "":
            users = AuthUser.objects.all()
        else:
            usersfirst = AuthUser.objects.filter(first_name__icontains=text)
            userslast = AuthUser.objects.filter(last_name__icontains=text)
            if len(usersfirst) >= len(userslast):
                users = usersfirst
            else:
                users = userslast
        for user in users:
            ans = {}
            ans["id"] = user.id
            ans["email"] = user.email
            ans["name"] = user.first_name + " " + user.last_name
            ans["username"] = user.username
            result.append(ans)
    except:
        pass
    try:
        result = sorted(result, key = lambda i: i["id"],reverse=True)
        return JsonResponse({'data':result}, safe=False)
    except:
        return JsonResponse({'status':'fail','message':'Something went wrong'})   

class tweet(APIView):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(tweet, self).dispatch(request, *args, **kwargs)

    # @permission_classes((IsAuthenticated, ))
    def post(self, request):
        email = ""
        message = ""
        try:
            b = request.body                
            body_json = json.loads(b)
            email = body_json['email']
            message = body_json['message']
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})
        try:
            check_user = AuthUser.objects.filter(email=email).exists()
            if check_user:
                user_id = AuthUser.objects.get(email=email).id
                Tweets.objects.create(user_id=user_id ,text=message)
                return JsonResponse({'status':'success','message':'Tweet added successfully'})
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong'})

    def get(self, request):
        id_list = [] 
        email = ""
        result = []
        user_id = ""
        try:
            email = request.GET.get('email')
        except:
            pass
        try:
            check_user = AuthUser.objects.filter(email=email).exists()
            if check_user:
                user_id = AuthUser.objects.get(email=email).id
                id_list.append(user_id)
                following = Follower.objects.filter(user_by=user_id)
                for i in following:
                    id_list.append(i.user_to)
                tweets = Tweets.objects.all()
                for tweet in tweets:
                    ans={}
                    if tweet.user_id in id_list:
                        ans["id"] = tweet.id
                        ans["user_id"] = tweet.user_id
                        ans["text"] = tweet.text
                        first = AuthUser.objects.get(id=tweet.user_id).first_name
                        last = AuthUser.objects.get(id=tweet.user_id).last_name
                        name = first +" "+last
                        ans["name"] = name
                        username =  AuthUser.objects.get(id=tweet.user_id).username
                        ans["username"] = username
                        likes = Likes.objects.filter(tweet_id = tweet.id).count()
                        ans["likes"] = likes
                        comment = Comment.objects.filter(tweet_id = tweet.id).count()
                        ans["comment"] = comment
                        check_like = Likes.objects.filter(tweet_id = tweet.id,user_id = user_id).exists()
                        if check_like:
                            ans["liked"] = True
                        else:
                            ans["liked"] = False
                        result.append(ans)
        except Exception as ex:
            return JsonResponse({'status':'fail','message':'Something went wrong',"data" : result})  
        try:
            result = sorted(result, key = lambda i: i["id"],reverse=True)
            return JsonResponse({'data':result}, safe=False)
        except:
            return JsonResponse({'status':'fail','message':'Something went wrong'})