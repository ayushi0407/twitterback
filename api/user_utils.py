from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from .utils import *
from django.core.files.storage import FileSystemStorage
import xlwt
import xlrd
from django.db.models import Q
import os
from django.contrib.auth import get_user_model

User = get_user_model()

def signup_user(f, l, e, ph, p): 
    try:
        u = e.split('@')[0]
        check_email = AuthUser.objects.filter(email=e).exists()
    except Exception as ex:
        return ({'status':'fail','message':str(ex)}) 
    
    if  check_email:
        return ({'status':'fail','message':'User with this email already exists'})    
    user_id=0
    try: 
        user = User.objects.create_user(username=u, email=e, password=p, is_staff=False)
        user.first_name = f
        user.last_name = l
        user.is_active = True
        user.save()        
        user_id = user.id
        auth_user = AuthUser.objects.get(id=user_id)
        auth_user.phonenumber = ph
        auth_user.save()
        token, created = Token.objects.get_or_create(user_id=user_id)
        token_key = token.key
        return ({'status':'success','message':'Successfully created your account.'})
    except Exception as ex:
        return ({'status':'fail','message':'Something went wrong'})  



