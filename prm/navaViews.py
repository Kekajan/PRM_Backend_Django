from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from prm.serializers import UserSettingPasswordSerializer ,UserSettingSerializer
from prm.models import Project, User, Task


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
def settingApi(request,id=0):
    if request.method == 'GET':
        if id:
            user = get_object_or_404(User, id=id)
            user_Setting_Serializer = UserSettingSerializer(user)
            return Response(user_Setting_Serializer.data)
        else:
            users = User.objects.all()
            user_Setting_Serializer = UserSettingSerializer(users, many=True)
            return Response(user_Setting_Serializer.data)

    elif request.method == 'PUT':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Product not found'}, status=404)

        data = JSONParser().parse(request)
        user_Setting_Serializer = UserSettingSerializer(user, data=data)

        if user_Setting_Serializer.is_valid():
            user_Setting_Serializer.save()


            return JsonResponse("Product Updated Successfully", safe=False)

        return JsonResponse(user_Setting_Serializer.errors, status=400)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_Setting_serializer = UserSettingSerializer(data=user_data)
        if user_Setting_serializer.is_valid():
            user_Setting_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'DELETE':
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("Deleted Successfully", safe=False)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
def settingasswordApi(request,id=0):
    if request.method == 'GET':
        if id:
            user = get_object_or_404(User, id=id)
            user_SettingPassword_Serializer = UserSettingPasswordSerializer(user)
            return Response(user_SettingPassword_Serializer.data)
        else:
            users = User.objects.all()
            user_SettingPassword_Serializer = UserSettingPasswordSerializer(users, many=True)
            return Response(user_SettingPassword_Serializer.data)

    elif request.method == 'PUT':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Product not found'}, status=404)

        data = JSONParser().parse(request)
        user_SettingPassword_Serializer = UserSettingPasswordSerializer(user, data=data)

        if user_SettingPassword_Serializer.is_valid():
            user_SettingPassword_Serializer.save()

            return JsonResponse("Product Updated Successfully", safe=False)

        return JsonResponse(user_SettingPassword_Serializer.errors, status=400)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_SettingPassword_Serializer = UserSettingPasswordSerializer(data=user_data)
        if user_SettingPassword_Serializer.is_valid():
            user_SettingPassword_Serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'DELETE':
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse("Deleted Successfully", safe=False)

# def settingasswordApi(request, id=0):
#     if request.method == 'GET':
#         if id:
#             user = get_object_or_404(User, id=id)
#             user_SettingPassword_Serializer = UserSettingPasswordSerializer(user)
#             return Response(user_SettingPassword_Serializer.data)
#         else:
#             users = User.objects.all()
#             user_SettingPassword_Serializer = UserSettingPasswordSerializer(users, many=True)
#             return Response(user_SettingPassword_Serializer.data)
# def settingasswordApi(request, id=0):
#     if request.method == 'PUT':
#         try:
#             user = User.objects.get(id=id)
#         except User.DoesNotExist:
#             return JsonResponse({'message': 'User not found'}, status=404)
#
#         data = JSONParser().parse(request)
#         # Ensure that the old password provided matches the user's current password
#         if not user.check_password(data.get('oldPassword', '')):
#             return JsonResponse({'message': 'Old password does not match'}, status=400)
#
#         # Update the password using set_password method
#         user.set_password(data.get('newPassword', ''))
#         user.save()
#
#         return JsonResponse("Password Updated Successfully", safe=False)