"""SES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from SES.views import RegisterUser, VerifyRegister, Login, LogoutUser, UserLoginStatus, \
    ForgotPassword, ResetPassword, UserInfo, ReadTemperature


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^SES/v1/auth/refresh/', refresh_jwt_token),
    url(r'^SES/v1/auth/token', obtain_jwt_token),
    url(r'^SES/v1/auth/status/(?P<User_Id>([0-9]+))$', UserLoginStatus.as_view(), name="userLoginStatus"),
    url(r'^SES/v1/auth/login/', Login.as_view(), name="login"),
    url(r'^SES/v1/auth/logout', LogoutUser.as_view(), name="logoutUser"),
    url(r'^SES/v1/auth/verify/(?P<Authorization_Code>([a-z]+))$', VerifyRegister.as_view(), name="verifyRegisterUser"),
    url(r'^SES/v1/auth/register/', RegisterUser.as_view(), name="registerUser"),
    url(r'^SES/v1/auth/forgotPassword/', ForgotPassword.as_view(), name="forgotPassword"),
    url(r'^SES/v1/auth/resetPassword/(?P<Authorization_Code>([a-z]+))$', ResetPassword.as_view(), name="resetPassword"),
    url(r'^SES/v1/key/(?P<ApiKey>([0-9]+))/$', ReadTemperature.as_view(), name="readTemperature"),
    url(r'^SES/v1/user/(?P<User_Id>([0-9]+))$', UserInfo.as_view(), name="userInfo"),
]
