from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.views import Token
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate

@api_view(['POST'])
@csrf_exempt
@parser_classes([JSONParser])

def RegisterApi(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user_data = data.get('user', {})
        user_data['password'] = make_password(user_data.get('password'))
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            email = user_data.get('email')
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "message": "Email already registered",
                }, status=400)            
            else:
                user_serializer = UserSerializer(data=user_data)               

                if user_serializer.is_valid():
                    user_instance = user_serializer.save()
                    token, created = Token.objects.get_or_create(user=user_instance)
                
                    user_info = {
                        "is_superuser": user_instance.is_superuser,
                        "first_name": user_instance.first_name,
                        "last_name": user_instance.last_name,
                        "email": user_instance.email,
                        "username": user_instance.username
                    }
                    return JsonResponse({
                        "user":user_info,
                        "token": token.key,
                        "message": True,
                    },status=200)
                user_instance.delete()
                return JsonResponse({

                    "error": user_serializer.errors
                }, status=400)

        return JsonResponse({
                "error": user_serializer.errors
            }, status=400)
    
    
@api_view(['POST'])
@parser_classes([JSONParser])
def LoginApi(request):
    if request.method == 'POST':
        data = request.data
        provided_token = request.META.get('HTTP_AUTHORIZATION')

        if data:
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                if created==False:
                    token.delete()
                    token = Token.objects.create(user=user)
                # Reserver = reserver.objects.filter(userId=user.id).first()

                user_info = {
                    "is_superuser": user.is_superuser,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email
                }                
                return JsonResponse({
                    "user": user_info,
                    "token": token.key,
                    "message": True,
                }, status=status.HTTP_200_OK)

            else:
                return JsonResponse({
                    'error': 'Invalid credentials or token',
                }, status=status.HTTP_401_UNAUTHORIZED)

        else:
            if provided_token and provided_token.startswith('Bearer '):
                token_key = provided_token.split(' ')[1]

                try:
                    token = Token.objects.get(key=token_key)
                    user = token.user

                    user_info = {
                        "is_superuser": user.is_superuser,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email
                    }

                    return JsonResponse({
                        "user": user_info,
                        "token": token.key,
                        "message": True,
                    }, status=status.HTTP_200_OK)

                except Token.DoesNotExist:
                    return JsonResponse({
                        "message": "Invalid token"
                    }, status=status.HTTP_401_UNAUTHORIZED)

        return JsonResponse({
            "message": "Token not provided or invalid format"
        }, status=status.HTTP_401_UNAUTHORIZED)