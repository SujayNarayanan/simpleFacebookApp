"""
Definition of views.
"""

from django.shortcuts import render,render_to_response,redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib import auth
from FbBasicInfo import settings
from app.models import MyAppUser
import urllib2
import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render_to_response('app/home.html',{'settings':settings})

def profile(request):
    assert isinstance(request, HttpRequest)
    code =  request.GET.dict()['code']
    accessTokenReq=urllib2.Request("https://graph.facebook.com/v2.3/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s"%(settings.FACEBOOK_APP_ID,settings.FACEBOOK_REDIRECT_URI,settings.FACEBOOK_APP_SECRET,code))
    accessTokenResponse=urllib2.urlopen(accessTokenReq)
    html=accessTokenResponse.read()
    json_obj=json.loads(html)
    access_token = json_obj['access_token']
    req=urllib2.Request("https://graph.facebook.com/me?access_token=%s"%access_token)
    res = urllib2.urlopen(req)
    html2=res.read()
    obj = json.loads(html2)
    username = obj['name']
    avatar = "http://graph.facebook.com/%s/picture?type=large"%obj['id']
    appUser = MyAppUser.objects.get_or_create(user_access_token=access_token,)[0]
    appUser.user_name = username
    appUser.user_avatar = avatar
    appUser.is_active = True
    appUser.save()
    return render_to_response('app/profile.html',{'username':username,'avatar':avatar,'appUser':appUser})

def logout(request,id):
    loggedOutUser = MyAppUser.objects.get(pk = id)
    loggedOutUser.is_active = False
    loggedOutUser.save()
    print "is active = false"
    return redirect('/')