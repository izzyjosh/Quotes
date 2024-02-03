from django.shortcuts import render
from .serializers import UserSerializer,NoteSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import authentication,permissions
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .models import Note

User = get_user_model()


#can only be accessed by the admin user
class UserList(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self,request:Request,format=None):
        users = User.objects.all()

        serializers = UserSerializer(users,many=True,context={"request":request})

        return Response(serializers.data,status=status.HTTP_200_OK)

#also by only the admin user
class UserDetail(APIView):

    permission_classes = ([permissions.IsAuthenticated,permissions.IsAdminUser])


    def get_object(self,pk):
        try:
            user = get_object_or_404(User,pk=pk)
            return user
        except user.DoesNotExists:
            return HttpResponse(status="404 not found")



    def get(self,request:Request,pk,format=None):

        user = self.get_object(pk)
        print(user)

        serializers = UserSerializer(user,context={"request":request})
        return Response(serializers.data,status=status.HTTP_200_OK)


    def put(self,request:Request,pk,format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user,request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=status.HTTP_201__CREATED)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)



#endpoint for registering new users
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



#This should be the homepage where all notes are to be displayed with a form also for creating notes
class NoteView(APIView):

    permission_classes = [permissions.IsAuthenticated]


    def get(self,request:Request,format=None):
        notes = Note.objects.filter(user=request.user)

        serializers = NoteSerializer(notes,many=True,context={"request":request})

        return Response(serializers.data,status=status.HTTP_200_OK)


    def post(self,request:Request,format=None):

        serializers = NoteSerializer(data=request.data,context={"request":request})
        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.error,status=status.HTTP_400_BAD_REQUEST)



#for viewing a particular notes and also for updating and deleting that note 
class NoteDetail(APIView):


    def get(self,request:Request,pk,format=None):
        note = get_object_or_404(Note,pk=pk)

        serializers = NoteSerializer(note,context={"request":request})
        return Response(serializers.data,status=status.HTTP_200_OK)


    def put(self,request:Request,pk,format=None):
        note = get_object_or_404(Note,pk=pk)

        serializers = NoteSerializer(note,request.data,context={"request":request})

        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.error,status=status.HTTP_400_BAD_REQUEST)



    def delete(self,request:Request,pk,format=None):
        note = get_object_or_404(Note,pk=pk)

        note.delete()
        data = {"deleted":"Note deleted successfully"}
        return Response(data,status=status.HTTP_204_NO_CONTENT)
