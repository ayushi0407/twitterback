from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
from django.http import HttpResponse, JsonResponse
import json
from datetime import datetime
from django.utils import timezone
import math
import random
import pytz
import requests
import string
from .models import *
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail,EmailMessage
from datetime import timedelta
from Crypto import Random
from Crypto.Cipher import AES
import os
from django.core.files.storage import default_storage
import traceback, sys
from django.template.loader import render_to_string

def user_response(status, message, email, token, role,loginflag,customer_id):
    data = {
        'status':status,
        'message':message,
        'email':email,
        'token':token,
        'role':role,
        'loginflag':loginflag,
        'customer_id':customer_id
    }    
    return JsonResponse(data, safe=False)

def formatted_date(dt):    
    try:        
        return dt.strftime('%b %d, %Y')
    except Exception as ex:        
        return dt

def formatted_datetime(dt):
    if dt:
        dt_tz = dt + timedelta(hours=5, minutes=30)    #corrected for time zone
        try:
            return dt_tz.strftime('%b %d, %Y %H:%M:%S')
        except Exception as ex:        
            return dt
    else:
        return None
