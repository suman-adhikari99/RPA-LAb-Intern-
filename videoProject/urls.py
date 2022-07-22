from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('videoApp.urls', namespace='videoApp')),
   

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# defaultUploadOptions = {
# "fieldname": "file",
# "validation": {
#   "allowedExts": ["mp4", "webm", "ogg"],
#   "allowedMimeTypes": ["video/mp4", "video/webm", "video/ogg"]
# }
# }