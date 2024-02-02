from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self,request:Request,format=None):
        users = User.objects.all()

        serializers = UserSerializer(users,many=True,context={"request":request})

        return Response(serializers.data,status=status.HTTP_200_OK)


class UserDetail(APIView):

    permission_classes = ([permissions.IsAuthenticated,permissions.IsAdminUser])

    def get_user(self,pk):
        try:
            user = get_object_or_404(User,pk=pk)
        except user.DoesNotExists:
            return HttpResponse(status="404 not found")


    def get(self,request:Request,pk,format=None):

        user = self.get_user(pk)

        serializers = UserSerializer(user,context={"request":request})
        return Response(serializers.data,status=status.HTTP_200_OK)

class RegisterUser(APIView):
    def post(self,request:Request,format=None):

        serializers = UserSerializer(data=request.data)

        data = {}
        if serializers.is_valid():
            user = serializers.save()

            password = request.data.get("password")

            data["username"] = user.username
            data["email"] = user.email
            token = Token.objects.get(user=user).key
            data["token"] = token

            current_user = get_object_or_404(User,email=user.email)
            current_user.set_password(password)
            current_user.save()
        else:
            data["error"] = "not authorised"
        return Response(data)


