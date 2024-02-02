from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Note
User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    password = serializers.CharField(min_length=8,write_only=True)

    class Meta:
        model = User
        fields = ("url","username","email","password")

    def validate(self,attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise ValidationError("user with this email already exists")
        return super().validate(attrs)


class NoteSerializer(serializers.HyperlinkedModelSerializer):

    #note = serializers.HyperlinkedRelatedField(many=True,read_only=True)
    class Meta:
        model = Note
        fields = ("url","title","audio_note","video_note","content","date")
