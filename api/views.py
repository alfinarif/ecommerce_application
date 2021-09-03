from django.shortcuts import render

# import serializer class from api.serializers
from api.serializers import RegistrationSerializer
# User model class
from accounts.models import User
# rest framework decorators functions
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
# rest framework permissions function
from rest_framework.permissions import AllowAny, IsAuthenticated
# rest framework authentication token class
from rest_framework.authtoken.models import Token
# rest framework json response class
from rest_framework.response import Response
# db error handeling class
from django.db import IntegrityError
# import json
import json
# this method will work to check password
from django.contrib.auth.hashers import check_password
# those method will work to user login and logout
from django.contrib.auth import login, logout

# user registration POST method functional api view
@api_view(["POST"])
@permission_classes([AllowAny])
def Register_Users(request):
    data = {}
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.save()
        token = Token.objects.get_or_create(user=account)[0].key
        data["message"] = "user registered successfully"
        data["email"] = account.email
        data["token"] = token
    else:
        data = serializer.errors
    return Response(data)


# user login POST method functional api view
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
        data = {}
        reqBody = json.loads(request.body)
        email = reqBody['email']
        print(email)
        password = reqBody['password']
        try:
            Account = User.objects.get(email=email)
        except BaseException as e:
            raise ValueError({"400": f'{str(e)}'})
        token = Token.objects.get_or_create(user=Account)[0].key
        print(token)
        if not check_password(password, Account.password):
            raise ValueError({"message": "Incorrect Login credentials"})
        if Account:
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["message"] = "user logged in"
                data["email_address"] = Account.email
                Res = {"data": data, "token": token}
                return Response(Res)
            else:
                raise ValueError({"400": f'Account not active'})
        else:
            raise ValueError({"400": f'Account doesnt exist'})

# user logout GET method functional api view
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')