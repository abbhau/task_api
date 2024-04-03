from django.shortcuts import render
from django.http import HttpResponse
from .serializers import UserSerializer, User, UserLoginSerializer, Task, TaskSerializer
from django.contrib.auth import authenticate
from rest_framework import generics
from .models import UserActivateToken
from rest_framework.views import APIView
import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import CustomUpdatePermission, CustomTaskCreate, CustomTaskDelete
from rest_framework.response import Response
from rest_framework.exceptions import APIException
logger = logging.getLogger('django')
from rest_framework.authtoken.models import Token



def generate_token(user):
        token, created = Token.objects.get_or_create(user=user)
        return ({'token': token.key})


class UserCreateRetrieve(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class =UserSerializer
    queryset = User.objects.all()


class UserUpdateAPI(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomUpdatePermission]
    serializer_class =UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPI(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class =UserSerializer
    queryset = User.objects.all()


class TaskCreateRetrieve(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomTaskCreate]
    serializer_class =TaskSerializer
    queryset = Task.objects.all()

class TaskDelete(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomTaskDelete]
    serializer_class =TaskSerializer
    queryset = Task.objects.all()


class TaskForDevelopers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self ,request):
        print("-----", request.user.role)
        if request.user.role == "developer":
            obj = Task.objects.filter(task_assigned_to = request.user.id)
            if obj:
                serializer = TaskSerializer(data=obj, many=True)
                if serializer.is_valid():
                    print("-----", serializer.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"msg":" Currently no task asigned for you"}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self ,request):
        if request.user.role == "developer":
            pk = request.query_params.get("task_id")
            print("pk", pk)
            try:
                obj = Task.objects.get(task_id=pk)
                if obj.task_assigned_to == request.user.id:
                    serializer = TaskSerializer(obj, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"msg":"You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                raise APIException(e)


class UserLoginview(APIView):

    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = generate_token(user)
                return Response({"token":token,'msg':"login success"},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':{'non_field_errors':['email or password is not valid']}}
                                ,status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

def verify_user(request, token):
    uats = UserActivateToken.objects.filter(act_link=token)
    if uats:
        for i in uats:
            logger.info("view i:", i)
            f = i.validate_user(token=token)
            return HttpResponse('<h3>verified</h3>')
    return HttpResponse('<h3>You are already verified or might be your token expired</h3>')


class UserLogOutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Invalidate the user's token
        request.auth.delete()

        return Response({'message': 'Logout successful'})
   




