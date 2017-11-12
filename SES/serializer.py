from SES.models import Register, RegisterStatus
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from SES.settings.base import \
    AUTHORIZATION_CODE_LENGTH, \
    LAST_NAME_LENGTH, \
    FIRST_NAME_LENGTH, \
    EMAIL_LENGTH

#  IntegerField, ReadOnlyField, SerializerMethodField, PrimaryKeyRelatedField
#  from django.contrib.auth.models import User


class RegisterStatusSerializer(ModelSerializer):
    Status = serializers.CharField(max_length=50, min_length=2, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = RegisterStatus
        fields = ('Id', 'Status')


class RegisterSerializer(ModelSerializer):
    Authorization_Code = serializers.CharField(max_length=AUTHORIZATION_CODE_LENGTH,
                                               min_length=AUTHORIZATION_CODE_LENGTH,
                                               required=False,
                                               allow_blank=True,
                                               trim_whitespace=True)
    Email = serializers.EmailField(max_length=EMAIL_LENGTH, min_length=6, allow_blank=False, trim_whitespace=True)
    First_Name = serializers.CharField(max_length=FIRST_NAME_LENGTH, min_length=3, allow_blank=False, trim_whitespace=True)
    Last_Name = serializers.CharField(max_length=LAST_NAME_LENGTH, min_length=3, allow_blank=False, trim_whitespace=True)
    User_Agent = serializers.CharField(max_length=255, required=False, min_length=0, allow_blank=True, trim_whitespace=True)
    IP_Address = serializers.IPAddressField(protocol='IPv4', required=False, allow_blank=True, trim_whitespace=True)
    Status_Id = RegisterStatusSerializer(required=False)

    class Meta:
        model = Register
        fields = ('Id', 'Email', 'First_Name', 'Last_Name', 'Authorization_Code', 'User_Agent', 'IP_Address', 'Status_Id')
