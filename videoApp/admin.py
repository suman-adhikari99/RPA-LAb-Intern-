from django.contrib import admin
from .models import User, VideoInformation,VideoUpload,ChargesOnVideo
 
# Register your models here.
admin.site.register(User)
admin.site.register(VideoInformation)
admin.site.register(VideoUpload)
admin.site.register(ChargesOnVideo)