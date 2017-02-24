from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import date, datetime, timedelta

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        regex_name = re.compile(r'^[a-zA-Z]{3,}$')
        regex_user = re.compile(r'^[a-zA-Z0-9]{3,}$')
        #check that everything's filled out
        for item in postData:
            if len(postData[item])<1:
                errors.append("empty")
                break
        try:
            user_exist = User.objects.get(email = postData['email'])
            errors.append('unique')
        except:
            pass

        # valFirst = nameRegex.match(postData['name'])

        if regex_name.match(postData['name']) == None:
            errors.append("name")
        if regex_user.match(postData['username']) == None:
            errors.append("username")
        if len(postData['password'])<8 or len(postData['conpassword'])<8:
            errors.append("passlength")
        if postData['password'] != postData['conpassword']:
            errors.append("passmatch")

        if len(errors)>0:
            return (False, errors)

        hashedPass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(name = postData['name'], username = postData['username'], pw_hash = hashedPass)
        print "New User Added", new_user.name
        return (True, new_user)

    def login(self, postData):
        errors = []
        print "Posted username", postData['username']
        try:
            user_exist = User.objects.get(username=postData['username'])
            print "Found the user", user_exist
            if bcrypt.hashpw(postData['password'].encode(), user_exist.pw_hash.encode()) == user_exist.pw_hash:
                return (True, user_exist)
            else:
                errors.append('password')
                return (False, errors)
        except:
            errors.append('absent')
            return (False, errors)


class User(models.Model):
    name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 45)
    pw_hash = models.CharField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class TravelPlanManager(models.Manager):
    def validate(self,postData):
        errors = []
        for item in postData:
            if len(postData[item])<1:
                errors.append("empty")
                break

class TravelPlan(models.Model):
    users = models.ManyToManyField(User)
    destination = models.CharField(max_length = 50)
    description = models.CharField(max_length = 50)
    travel_start = models.DateTimeField(auto_now = False)
    travel_end = models.DateTimeField(auto_now = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TravelPlanManager()


