from rest_framework import generics, status
import json
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from SES.serializer import RegisterSerializer, RegisterStatusSerializer
import logging
from SES.models import CustomUser, Register, RegisterStatus, UserStatus, PasswordStatus, \
    EmailAddress, EmailAddressStatus, NameType, Name, PasswordReset, PasswordResetStatus, UserLogin
from rest_framework.authentication import BasicAuthentication
from ipware.ip import get_ip
from SES.settings.base import REGISTER_STATUS, AUTHORIZATION_CODE_LENGTH, PASSWORD_STATUS, \
    USER_STATUS, EMAIL_ADDRESS_STATUS, NAME_TYPE, PASSWORD_LENGTH, PASSWORD_RESET_STATUS
from random import choice
import string
import pytz
from datetime import datetime, timedelta
from SES.classes.myEmail import MyEmail
from SES.classes.UserUtil import Util
from SES.classes.EmailUtil import EmailUtil
from SES.classes.utils import ReturnResponse
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings

logger = logging.getLogger(__name__)


class UserInfo(generics.ListAPIView):
    model = CustomUser
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_id = kwargs.get('User_Id', 0)
            user = CustomUser.objects.get(pk=user_id)
            result = "email:{0}".format(user.Email)
            logger.debug(result)
            return Response(ReturnResponse.Response(0, __name__, 'success', result).return_json(), status=status.HTTP_200_OK)


class UserLoginStatus(generics.ListAPIView):
    model = CustomUser
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_id = kwargs.get('User_Id', 0)
            user = CustomUser.objects.get(pk=user_id)
            result = "email:{0}".format(user.Email)
            logger.debug(result)
            return Response(ReturnResponse.Response(0, __name__, 'success', result).return_json(), status=status.HTTP_200_OK)


class ReadTemperature(generics.CreateAPIView):
    model = CustomUser
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        apiKey = kwargs.get('ApiKey', 0)
        tempHumidity = 0
        data = ""

        try:
            print(request.body.decode("utf-8"))
            tempHumidity = json.loads(request.body.decode("utf-8"))
            result = 'Parsed JSON:{0}'.format(tempHumidity)
            logger.debug(result)
        except:
            result = 'Failed to parse JSON:{0}'.format(request.body.decode("utf-8"))
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)
        try:
            print('API Key=' + apiKey)
            print('temp=' + tempHumidity['temperature'])
            print('humidity=' + tempHumidity['humidity'])
            return Response(ReturnResponse.Response(0, __name__, 'success', "done").return_json(), status=status.HTTP_200_OK)
        except:
            result = 'failed reading data'
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)



class RegisterUser(generics.CreateAPIView):
    model = Register
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = (BasicAuthentication,)
    parser_classes = (JSONParser,)

    def get_authorization_code(self):
        letters = string.ascii_lowercase
        authorization_code = ''.join(choice(letters) for i in range(AUTHORIZATION_CODE_LENGTH))
        logger.debug(authorization_code)
        return authorization_code

    def post(self, request, *args, **kwargs):

        try:
            data = JSONParser().parse(request)
            result = 'Parsed JSON:{0}'.format(data)
            logger.debug(result)
        except:
            result = 'Failed to parse JSON:{0}'.format(request)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        try:
            validate_email(data['register_data']['Email'])
            result = 'Email Address Valid:{0}'.format(data['register_data']['Email'])
            logger.debug(result)
        except validate_email.ValidationError:
            result = 'Email Address not Valid:'.format(data['register_data'])
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        email_util = EmailUtil()
        if email_util.find_email(data['register_data']['Email']) != 0:
            result = 'Email Address Already Exists:'.format(data['register_data'])
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())
        else:
            result = 'Email Address Available:{0}'.format(data['register_data']['Email'])
            logger.debug(result)

        serializer = RegisterSerializer(data=data['register_data'])
        if serializer.is_valid():
            new_register_status = RegisterStatus.objects.get(pk=REGISTER_STATUS['NEW'])
            serializer.save(User_Agent=request.user_agent.browser,
                            IP_Address=get_ip(request),
                            Authorization_Code=self.get_authorization_code(),
                            Status_Id=new_register_status)
            my_email = MyEmail('Verify Email')
            result = my_email.send_verify_email(serializer.data['Id'])
            logger.debug(result)
            status_serializer = RegisterStatusSerializer(new_register_status)
            result = status_serializer.data
            logger.debug(result)
            return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),  status=status.HTTP_201_CREATED)
        else:
            result = serializer.errors
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),  status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    parser_classes = (JSONParser,)

    def get_authorization_code(self):
        letters = string.ascii_lowercase
        authorization_code = ''.join(choice(letters) for i in range(AUTHORIZATION_CODE_LENGTH))
        logger.debug(authorization_code)
        return authorization_code

    def post(self, request, *args, **kwargs):
        try:
            data = JSONParser().parse(request)
            result = 'parsed Email:{0} from:{1}'.format(data['email'], data)
            logger.error(result)
        except:
            result = 'Failed Parsing Email from:{0}'.format(request)
            logger.debug(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        try:
            validate_email(data['email'])
            result = 'Validated Email :{0}'.format(data['email'])
            logger.debug(result)
            email = data['email']
        except:
            result = 'Failed Validating Email :{0}'.format(data['email'])
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        try:
            custom_user = CustomUser.objects.get(Email=email)
            result = 'Retrieved custom user email:{0}'.format(custom_user.Email)
            logger.debug(result)
        except ObjectDoesNotExist:
            email_address_status = EmailAddressStatus.objects.get(pk=EMAIL_ADDRESS_STATUS['NOTFOUND'])
            result = {'status': 1, 'reason':  email_address_status.Status}
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        if not custom_user.is_active:
            result = {'status': 1, 'reason': 'Email Address not Active'}
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        try:
            PasswordReset.objects.get(Status_Id=PasswordResetStatus(pk=PASSWORD_RESET_STATUS['ACTIVE']),
                                      User_Id=custom_user.Id)
            result = 'Found password reset in table:{0}'.format(PasswordReset.Id)
            logger.debug(result)
        except ObjectDoesNotExist:
            password_reset = PasswordReset()
            password_reset.Authorization_Code = self.get_authorization_code()
            password_reset.User_Id = custom_user
            password_reset.Status_Id = PasswordResetStatus(pk=PASSWORD_RESET_STATUS['ACTIVE'])
            password_reset.save()
            result = 'created password_reset in table:{0}'.format(PasswordReset.User_Id)
            logger.debug(result)

        my_mail = MyEmail("Forgot Password")
        result = my_mail.send_forgot_password_email(custom_user)
        return Response(ReturnResponse.Response(0, __name__, 'success', result).return_json())


class ResetPassword(generics.ListAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = (BasicAuthentication,)
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):
        authorization_code = kwargs.get('Authorization_Code', 0)

        my_email = MyEmail('Send New Password')
        result = my_email.send_reset_password_email(authorization_code)

        return Response(ReturnResponse.Response(0, __name__, 'success', result).return_json(), status=status.HTTP_200_OK)


class LogoutUser(generics.ListAPIView):
    model = Register
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = (BasicAuthentication,)
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):
        result = "logged out"
        return Response(ReturnResponse.Response(0, __name__, 'success', result).return_json(),
                        status=status.HTTP_200_OK)


class Login(generics.CreateAPIView):
    model = UserLogin
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = (BasicAuthentication,)
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        userLogin = UserLogin()
        try:
            data = JSONParser().parse(request)
            result = 'parsed json:{0}'.format(data)
            logger.debug(result)
        except:
            result = 'Could not Retrieve email and/or password'
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        try:
            email = data['email']
            result = 'parsed email:{0}'.format(email)
            logger.debug(result)
        except:
            result = 'Could not parse email{0}'.format(data)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        try:
            password = data['password']
            result = 'parsed password:{0}'.format(password)
            logger.debug(result)
        except:
            result = 'Could not Retrieve password'.format(data)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        try:
            user = CustomUser.objects.get(Email=email)
            result = 'Retrieved user address:{0} and userId:{1}'.format(user.Email,user.Id)
            logger.debug(result)
        except ObjectDoesNotExist:
            email_address_status = EmailAddressStatus.objects.get(pk=EMAIL_ADDRESS_STATUS['NOTFOUND'])
            result = email_address_status.Status
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        if not user.is_active:
            result = 'Email Address not Active: {0}'.format(user.is_active)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())

        if user.check_password(password):
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            result = jwt_encode_handler(payload)
            logger.debug(result)
            user.is_logged_in = True
            return Response(ReturnResponse.Response(0, __name__, 'success', result).return_json(), status=status.HTTP_200_OK)
        else:
            password_status = PasswordStatus.objects.get(pk=PASSWORD_STATUS['FAILED'])
            result = 'Wrong Password:' + password_status.Status
            user.is_logged_in = False
            logger.error(result)
        return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json())


class VerifyRegister(generics.ListAPIView):
    model = Register
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    authentication_classes = (BasicAuthentication,)
    queryset = Register.objects.all()
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):

        authorization_code = kwargs.get('Authorization_Code', 0)

        try:
            self.get_queryset().filter(Authorization_Code=authorization_code).count()
            verify_register = Register.objects.get(Authorization_Code=authorization_code)
        except ObjectDoesNotExist:
            register_status = RegisterStatus.objects.get(pk=REGISTER_STATUS['INVALID'])
            result = 'Invalid Register Code:{0} :{1}'.format(register_status.Status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        if verify_register.Status_Id.pk == REGISTER_STATUS['EXPIRED']:
            result = 'Expired Register Code:{0} :{1}'.format(verify_register.Status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        if verify_register.Status_Id.pk == REGISTER_STATUS['VERIFIED']:
            result = 'Already Verified Register Code:{0} :{1}'.format(verify_register.Status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        if verify_register.Status_Id.pk == REGISTER_STATUS['NEW']:
            result = 'New Register Code:{0} :{1}'.format(verify_register.Status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        if verify_register.Status_Id.pk != REGISTER_STATUS['SENT']:
            result = 'Register Code Already Sent:{0} :{1}'.format(verify_register.Status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        if (pytz.utc.localize(datetime.utcnow()) - verify_register.Inserted) > timedelta(1):
            register_status = RegisterStatus.objects.get(pk=REGISTER_STATUS['EXPIRED'])
            verify_register.Status_Id = register_status
            verify_register.save()
            result = 'Register Code Expired:{0} :{1}'.format(verify_register.Status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        new_user = CustomUser(Status_Id=UserStatus.objects.get(pk=USER_STATUS['ACTIVE']))
        user_util = Util()
        if user_util.find_username(verify_register.First_Name + verify_register.Last_Name) != 0:
            result = 'Failed creating username: already exists'
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        email_util = EmailUtil()
        if email_util.find_email(verify_register.Email) != 0:
            email_status = EmailAddressStatus.objects.get(pk=EMAIL_ADDRESS_STATUS['EXISTS'])
            result = 'Email Already exists:{0}: {1}:'.format(email_status.Status, verify_register.Email)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'failed', result).return_json(), status=status.HTTP_200_OK)

        new_user.Email = verify_register.Email
        new_user.Username = user_util.new_username
        pw = self.generate_password()
        new_user.set_password(pw)
        new_user.save()

        email = EmailAddress(Email=verify_register.Email,
                             User_Id=new_user,
                             Status_Id=EmailAddressStatus(pk=EMAIL_ADDRESS_STATUS['ACTIVE']))

        first_name = Name(Name=verify_register.First_Name,
                    Type_Id=NameType.objects.get(pk=NAME_TYPE['FIRST']),
                    User_Id=new_user)

        last_name = Name(Name=verify_register.Last_Name,
                    Type_Id=NameType.objects.get(pk=NAME_TYPE['LAST']),
                    User_Id=new_user)

        email.save()
        first_name.save()
        last_name.save()

        my_mail = MyEmail("Welcome Email")
        my_mail.send_welcome_email(new_user, pw)

        verify_register.Status_Id = RegisterStatus.objects.get(Id=REGISTER_STATUS['VERIFIED'])
        verify_register.save()

        result = 'New User Added:{0}:'.format(new_user.pk)
        logger.info(result)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(), status=status.HTTP_200_OK)

    def generate_password(self):
        letters = string.ascii_lowercase
        new_password = ''.join(choice(letters) for i in range(PASSWORD_LENGTH))
        result = 'Generated new Password:{0}'.format(new_password)
        logger.debug(result)
        return new_password
