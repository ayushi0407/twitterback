from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

class AuthUser(AbstractUser):    
    phonenumber = models.CharField(max_length=255) 

class Tweets(models.Model):
    id = models.AutoField(primary_key=True) 
    user_id = models.IntegerField(blank=True, null=True)
    text = models.TextField()
    class Meta:
        managed = True
        db_table = 'tweet'

class Follower(models.Model):
    id = models.AutoField(primary_key=True) 
    user_by = models.IntegerField(blank=True, null=True)
    user_to = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'follower'

class Likes(models.Model):
    id = models.AutoField(primary_key=True) 
    user_id = models.IntegerField(blank=True, null=True)
    tweet_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'likes'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    tweet_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    text = models.TextField()
    
    class Meta:
        managed = True
        db_table = 'comment'

