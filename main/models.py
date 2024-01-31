from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 

class User(AbstractUser):
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False,
            )
    username = models.CharField(max_length=200,unique=True)
    email = models.EmailField()

    USERNAME_FIELD = ("username")
    REQUIRED_FIELD = ("email")

    def __str__(self):
        return self.username


class Note(models.Model):
    title:str = models.CharField(max_length=300)
    audio_note = models.FileField(upload_to="audio_note",blank=True,null=True)
    video_note = models.FileField(upload_to="video_note",blank=True,null=True)
    content:str = models.TextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    user:User = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.title


class NoteShared(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Notes Shared"

    def __str__(self):
        return self.note.title
