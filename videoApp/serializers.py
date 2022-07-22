from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.template.defaultfilters import filesizeformat
from django.conf import settings


class UserPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name',  'contact_no', 'email', 'username', 'password','contact_no']
        extra_kwargs = {
            "password": {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


class videoUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoUpload
        fields = ['file']
        extra_kwargs = {
            "file": {'required': True},
        }

    def validate(self, data):
        content = data['file']
        content_type = content.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if content.size > settings.MAX_UPLOAD_SIZE:
                raise serializers.ValidationError(
                         {"exceed_file_size": "Your File Size Is More Than 1 GB"})
        else:
            raise serializers.ValidationError(
                {"invalid_content_type": "Only Video File Are Supperted"})
        return super().validate(data)


class videoInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoInformation
        fields="__all__"
       
    def validate(self, data):
        if data.get('duration')>10:
            raise serializers.ValidationError(
                         {"exceed_length": "Duration Of Video Is More Than 10 Minutes"})
        return super().validate(data)



class ChargeOnVideoSerializer(serializers.ModelSerializer):
    size=serializers.IntegerField(max_value=1024, min_value=1)  # size of video is asssume as MB
    length=serializers.DecimalField(max_value=10,max_digits=2,decimal_places=1)
    class Meta:
        model = ChargesOnVideo
        fields=['type','size','length']
       
