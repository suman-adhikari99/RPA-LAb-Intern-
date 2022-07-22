# from django.db.models import FileField
# from django.forms import forms
# from django.template.defaultfilters import filesizeformat
# from django.utils.translation import gettext as _
# class ContentTypeRestrictedFileField(FileField):
    
#     def __init__(self, content_types=None,max_upload_size=104857600, **kwargs):
#         self.content_types = kwargs.pop( 'video/mp4','video/mkv', )
#         self.max_upload_size = max_upload_size

#         super(ContentTypeRestrictedFileField, self).__init__(**kwargs)


#     def clean(self, *args, **kwargs):        
#         data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

#         file = data.file
#         try:
#             content_type = file.content_type
#             print("content TYpe is ",self.content_types)
#             if content_type in self.content_types:
#                 if file._size > self.max_upload_size:
#                     print("file size is",self.max_upload_size)

#                     raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
#             else:
#                 raise forms.ValidationError(_('Filetype not supported.'))
#         except AttributeError:
#             pass        

#         return data

        