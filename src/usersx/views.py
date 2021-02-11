from django.shortcuts import render
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer

import json
import jwt
import logging
import datetime

# Expiration time for the authentication token (5 mins)
EXP_TIME = datetime.timedelta(minutes=5)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG,)

@api_view(['GET'])
def list_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


def get_token(username):
    try:
        user = User.objects.get(username=username)
        if user:
            try:
                payload = {'id': user.id, 'username': user.username,
                           'exp': datetime.datetime.utcnow()+EXP_TIME}
                secret = settings.AUTH_TOKEN
                encoded = jwt.encode(payload, secret, algorithm = "HS256")
                #jwt.decode(encoded, secret, algorithms = ['HS256'])
                token = {'token': encoded}
                return token
            except Exception as e:
                error = {'error_code': status.HTTP_400_BAD_REQUEST,
                         'error_message': "Encountered an error while generating a token."}
                logger.error(e)
                return Response(error, status=status.HTTP_403_FORBIDDEN)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_Message': "Invalid Username or Password"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_Message': "Internal Server Error"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


def auth(request, username):
    try:
        token = request.session.get('authtoken').get('token')
        payload = jwt.decode(token, settings.AUTH_TOKEN)
        user = User.objects.get(username=username)
        if payload.get('username') == user.username:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_403_FORBIDDEN,
                     'Error_Message': "Invalid User"}
            logger.error(error)
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError) as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                 'Error_Message': "Token is Invalid/Expired"}
        logger.error(e)
        return Response(error, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                 'Error_Message': "Internal Server Error"}
        logger.error(e)
        return Response(error, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def login(request, username=None, password=None):
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    try:
        user = User.objects.get(username=username)
        if user.password == password:
            token = get_token(username)
            user.token = token['token']
            user.save()
            request.session['authtoken'] = token
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_message': "Invalid Username or Password."}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                 'Error_message': "Invalid Username."}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signup(request):
    try:
        serializer = UserSerializer(data=request.query_params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST, 
                    'Error_message': "Error occured while creating account."}
            return Response(error, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                     'Error_message': "Error occured while creating account."}
            logger.error(e)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def follow(request,loggedin_user,user):
    try:
        cur_user=User.objects.get(username=loggedin_user)
        fol_user=User.objects.get(username=user)
        cur_user.following.add(fol_user)
        cur_user.save()
        serializer = UserSerializer(cur_user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Request Failed. Invalid Details"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)  


@api_view(['GET'])
def get_followers(request, username):
    try:
        user = User.objects.get(username=username)
        followers = user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User does not exist"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)            

@api_view(['GET'])
def get_following(request, username):
    try:
        user = User.objects.get(username=username)
        following = user.following.all()
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User does not exist"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST) 
