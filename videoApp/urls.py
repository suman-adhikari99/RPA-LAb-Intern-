from django.urls import path
from .views import *
app_name = "videoApp"

urlpatterns = [
    
    path("user/register", RegisterView.as_view()),
    path("user/login", LoginView.as_view()),
    path("upload-video", UploadVideo.as_view()),
    path("api/get", GetVideo.as_view()),
    path("api/get/<int:pk>", GetVideo.as_view()),
    path("api/filter", UploadedVideoFilter.as_view()),
    path("api/charge", CalculateCharge.as_view()),

]
