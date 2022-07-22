
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from .serializers import *
from moviepy.editor import *
from utils.api_render_response import api_response_render
from utils.auth_decorator import auth_required
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters
import operator
from django.db.models import Q
from functools import reduce

# Create your views here.4


class UploadVideo(APIView):
    @auth_required()
    def post(self, request,user_id):
        try:
            serializer=videoUploadSerializer(data=request.FILES)
            if serializer.is_valid():
                serializer.save()
            else:
                return api_response_render(status_msg=serializer.errors, status_type='Error', status_code=400) 
            data1={}
            file=request.FILES.get("file",None)
            data1['type'] = file.content_type.split('/')[0]
            data1['size']=file.size/1024 # video size in mb
            data1['user']=user_id
            
            files=VideoUpload.objects.last()
            video = VideoFileClip(settings.MEDIA_ROOT+ files.file.name)
            data1['duration']=video.duration/60  # this will return the length of the video in min
            data1['name']=files.file.name[:30]
            data1['video']=files.id
            serializerv=videoInformationSerializer(data=data1)
            if serializerv.is_valid():
                serializerv.save()
                return api_response_render(status_msg="SuccessFully Uploaded", status_type='Success', status_code=201)    
            return api_response_render(status_msg=serializerv.errors, status_type='Error', status_code=400) 
        except Exception as e:
            return api_response_render(status_msg=str(e), status_type='Error', status_code=500)

        

class GetVideo(APIView):
    def get(self, request, pk=None):
        try:
            if pk == None:
                data = VideoInformation.objects.all()
                serialized_data=videoInformationSerializer(data,many=True).data
            else:
                data=VideoInformation.get_video_information(pk)
                serialized_data=videoInformationSerializer(data).data
            return api_response_render(data=serialized_data, status_msg="Data Fetch Sucessfully", status_type='Success', status_code=200)
        except Exception as e:
            return api_response_render(status_msg=str(e), status_type='Error', status_code=500)
    


class UploadedVideoFilter(generics.ListAPIView):
    queryset = VideoInformation.objects.all()
    serializer_class = videoInformationSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['id', 'created','name','duration','size']
    search_fields = [ 'id','created','name','duration','size']
    ordering_fields=['id','created','name','duration','size']



class CalculateCharge(APIView):
    def get(self,request):
        serializer=ChargeOnVideoSerializer(data=request.data)
        if serializer.is_valid():
            length=request.data.get('length',None)
            size=float(request.data.get('size',None))
            type=request.data.get('type',None)
            q_list = [Q(min_size__lte=size,max_size__gte=size),Q(min_length__lte=length,max_length__gte=length), Q(type__iexact=type)]
            response={
                "charge":ChargesOnVideo.objects.filter(reduce(operator.and_, q_list)).first().charge
                }
            return api_response_render(data=response, status_type='Success', status_code=200) 
        return api_response_render(status_msg=serializer.errors, status_type='Error', status_code=400) 



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            data["username"] =data.get('email')
            serializer = UserPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return api_response_render(status_msg="SuccessFully Registered", status_type='Success', status_code=201)    
            return api_response_render(status_msg=serializer.errors, status_type='Error', status_code=400)    
        except Exception as e:
            return api_response_render(status_msg=str(e), status_type='Error', status_code=500)

    
class LoginView(APIView):
    
    def post(self, request):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active :
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["access"],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                )
                user.save()
                csrf.get_token(request)
                response.data = {"Success" : "Login successful","data":data}
                return response
            return api_response_render(status_msg=f"This account is not verified. ", status_type='Error', status_code=400)
        else:
            return api_response_render(status_msg="Invalid username or password!!", status_type='Error', status_code=400)

    def delete(self, request):
        response = Response()
        response.delete_cookie('access_token')
        response.data = {"message" : "User Session Deletion"}
        return response 

