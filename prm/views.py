from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from prm.serializers import ProjectSerializer, UserSerializer, TaskSerializer, UsernameSerializer
from prm.models import Project, User, Task
from django.contrib.auth.hashers import make_password


@csrf_exempt
def projectApi(request, id=0):
    if request.method == 'GET':
        project = Project.objects.all()
        project_serializer = ProjectSerializer(project, many=True)
        return JsonResponse(project_serializer.data, safe=False)

    elif request.method == 'POST':
        project_data = JSONParser().parse(request)
        project_serializer = ProjectSerializer(data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)

    elif request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project = Project.objects.get(id=id)
        project_serializer = ProjectSerializer(project, data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")

    elif request.method == 'DELETE':
        project = Project.objects.get(id=id)
        project.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def signup(request, id=0):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_data['password'] = make_password(user_data['password'])
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Signup Successfully", safe=False)
        else:
            return JsonResponse({"error": user_serializer.errors}, safe=False)

    elif request.method == 'GET':
        user = User.objects.all()
        user_serializer = UserSerializer(user, many=True)
        return JsonResponse(user_serializer.data, safe=False)


class AuthToken:
    objects = None


@api_view(['POST', 'GET'])
def login_user(request):
    if request.method == 'POST':
        try:
            username = request.data.get('userName')
            password = request.data.get('password')

            user = get_user_model().objects.filter(username=username).first()
            # print(user)

            if user is None:
                raise AuthenticationFailed("User not found")

            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect password")

            _, token = AuthToken.objects.create(user)
            user.is_active = True
            user.save()
            response_data = {
                'user_info': {
                    'userName': user.username,
                    'password': user.password
                },
                'token': token,
                'message': 'Login successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except KeyError:
            return Response({
                "details": "error"
            }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response({
            "details": "Method not allowed"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
def taskApi(request, id=None):
    if request.method == 'GET':
        if id is not None:
            task = get_object_or_404(Task, id=id)
            task_serializer = TaskSerializer(task)
            return JsonResponse(task_serializer.data, safe=False)
        else:
            task = Task.objects.all()
            task_serializer = TaskSerializer(task, many=True)
            return JsonResponse(task_serializer.data, safe=False)

    elif request.method == 'POST':
        task_data = JSONParser().parse(request)
        task_serializer = TaskSerializer(data=task_data)
        if task_serializer.is_valid():
            task_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)


    elif request.method == 'PUT':
        if id is not None:
            task = get_object_or_404(Task, id=id)
            task_data = JSONParser().parse(request)
            task_serializer = TaskSerializer(task, data=task_data)
            if task_serializer.is_valid():
                task_serializer.save()
                return JsonResponse("Updated Successfully", safe=False)
            return JsonResponse("Failed to Update", status=400)

        else:
            task = Task.objects.all()
            task_data_list = JSONParser().parse(request)
            for task_data in task_data_list:
                task_id = task_data.get('id')
                task = get_object_or_404(Task, id=task_id)
                task_serializer = TaskSerializer(task, data=task_data)
                if task_serializer.is_valid():
                    task_serializer.save()
                else:
                    return JsonResponse("Failed to Update", status=400)
            return JsonResponse("Updated Successfully", safe=False)

    elif request.method == 'DELETE':
        task = Task.objects.get(id=id)
        task.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def usernameApi(request):
    if request.method == 'GET':        
        # usernames = User.objects.values_list('userName', flat=True)
        usernames = User.objects.values('userName')
        username_serializer = UsernameSerializer(usernames, many=True)
        return JsonResponse(username_serializer.data, safe=False)
   
@csrf_exempt
def taskProjectApi(request, id=None):
    if request.method == 'GET':
        if id is not None:
            task = Task.objects.filter(projectid=id)
            task_serializer = TaskSerializer(task, many=True)
            return JsonResponse(task_serializer.data, safe=False)
        