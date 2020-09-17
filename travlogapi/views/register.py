from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from travlogapi.models import Traveler
import json

@csrf_exempt
def login_user(request):

    req_body = json.loads(request.body.decode())

    if request.method == 'POST':
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_user(request):
    
    req_body = json.loads(request.body.decode())
    try:
        new_user = User.objects.create_user(
            username = req_body['username'],
            email = req_body['email'],
            password = req_body['password'],
            first_name = req_body['first_name'],
            last_name = req_body['last_name']
        )

        new_traveler = Traveler.objects.create(
            bio = req_body['bio'],
            user = new_user
        )

        token = Token.objects.create(user=new_user)
        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')
    except Exception as ex:
        return HttpResponseServerError(ex)