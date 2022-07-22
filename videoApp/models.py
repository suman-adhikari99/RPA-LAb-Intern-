from django.contrib.auth.models import AbstractUser
from django.db import models
import jwt
from videoProject.settings import SIMPLE_JWT
from rest_framework.exceptions import NotFound
from django.core.validators import FileExtensionValidator


# Create your models here.
class CreatedUpdatedBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.email+str(self.id))

    @property
    def full_name(self):
        return ' '.join(filter(None, (self.first_name, self.middle_name, self.last_name)))

    @classmethod
    def user_from_token(self, token):
        user = jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[
                          SIMPLE_JWT['ALGORITHM']],)
        return user


class VideoUpload(models.Model):
    file = models.FileField(null=True, 
                           blank=True, 
                           validators=[FileExtensionValidator( ['mp4','mkv'] ) ])
    
    def __str__(self):
        return f"{self.file}!!"
        

class VideoInformation(CreatedUpdatedBase):
    video=models.OneToOneField(to="VideoUpload",on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    size=models.FloatField(null=True, blank=True)
    duration=models.FloatField(null=True,blank=True)
    type=models.CharField(max_length=40,null=True, blank=True)

    @classmethod
    def get_video_information(cls,pk):
        try:
            return cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            raise NotFound("VideoInformation_DOESNOT_EXIST")

    def __str__(self):
        return f"{self.name},{self.user.first_name},"


class ChargesOnVideo(models.Model):
    charge=models.FloatField()
    min_size=models.FloatField()
    max_size=models.FloatField()
    min_length=models.FloatField()
    max_length=models.FloatField()
    type=models.CharField(max_length=40)

    def __str__(self):
        return f'Charge of video is  {self.charge}, min size of video-{self.min_size} max size of video-{self.max_size} and length of video-{self.type}'