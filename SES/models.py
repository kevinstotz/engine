from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from SES.settings.base import \
    EMAIL_TEMPLATE_DIR, \
    AUTHORIZATION_CODE_LENGTH, \
    LAST_NAME_LENGTH, \
    FIRST_NAME_LENGTH, \
    EMAIL_LENGTH
#    AUTH_USER_MODEL, \
from .managers import UserManager

class UserStatus(models.Model):
    Id = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=50, verbose_name="Status of User")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "User Status"

    class Meta:
        ordering = ('Id',)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    Id = models.AutoField(primary_key=True)
    Email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              verbose_name="Login email of user",
                              unique=True)
    Username = models.CharField(max_length=50, verbose_name="User name")
    Status_Id = models.ForeignKey(UserStatus, on_delete=models.SET_DEFAULT, default=0)
    Inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    is_active = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)
    is_staff = models.BooleanField( default=True)
    Avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    class Meta:
        ordering = ('Id',)

    def __str__(self):
        return '%s' % "User"

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = [Email]

    def get_full_name(self):
        full_name = '%s %s' % ("first", "last")
        return full_name.strip()

    def get_short_name(self):
        return "first"



class RegisterStatus(models.Model):
    Id = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=50, verbose_name="Status of Register")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "RegisterStatus"

    class Meta:
        ordering = ('Id',)


class EmailAddressStatus(models.Model):
    Id = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=50, verbose_name="Status of Email Address")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "EmailAddressStatus"

    class Meta:
        ordering = ('Id',)


class NotificationStatus(models.Model):
    Id = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=50, verbose_name="Status of Notification")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "NotificationStatus"

    class Meta:
        ordering = ('Id',)


class Role(models.Model):
    Id = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=50, verbose_name="Role of User")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Role"

    class Meta:
        ordering = ('Id',)


class PasswordStatus(models.Model):
    Id = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=72, verbose_name="Status of Password")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Passwword Status"

    class Meta:
        ordering = ('Id',)


class LoginStatus(models.Model):
    Id = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=50, verbose_name="Status of Login")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Login Status"

    class Meta:
        ordering = ('Id',)


class PasswordResetStatus(models.Model):
    Id = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=50, verbose_name="Status of Password Reset")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Password Reset Status"

    class Meta:
        ordering = ('Id',)




class NameType(models.Model):
    Id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Type of Name")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "NameTypes"

    class Meta:
        ordering = ('Id',)


class NotificationType(models.Model):
    Id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=50, verbose_name="Type of Notification")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "NotificationTypes"

    class Meta:
        ordering = ('Id',)


class Register(models.Model):
    Id = models.AutoField(primary_key=True)
    Email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email of Register")
    First_Name = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="First Name of Register")
    Last_Name = models.CharField(max_length=LAST_NAME_LENGTH, verbose_name="Last Name of Register")
    IP_Address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP Address of Register")
    User_Agent = models.CharField(max_length=255, blank=True, verbose_name="User Agent of Register")
    Authorization_Code = models.CharField(max_length=AUTHORIZATION_CODE_LENGTH,
                                          blank=False,
                                          verbose_name="Auto Generated Auth Code")
    Inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    Status_Id = models.ForeignKey(RegisterStatus, on_delete=models.SET_DEFAULT, default=0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Registered"

    class Meta:
        ordering = ('Id',)


class EmailTemplate(models.Model):
    Id = models.AutoField(primary_key=True)
    Subject = models.CharField(max_length=60, verbose_name="Subject of Email")
    From = models.CharField(max_length=50, verbose_name="From Username")
    HTML_Filename = models.FileField(upload_to=EMAIL_TEMPLATE_DIR,
                                     max_length=100,
                                     blank=True,
                                     null=True,
                                     verbose_name="Filename")
    TXT_Filename = models.FileField(upload_to=EMAIL_TEMPLATE_DIR,
                                    max_length=100,
                                    blank=True,
                                    null=True,
                                    verbose_name="Filename")
    objects = models.Manager()

    @property
    def HTML_name(self):
        return self.HTML_Filename.name

    @property
    def TXT_name(self):
        return self.TXT_Filename.name

    def __str__(self):
        return '%s' % "EmailTemplates"

    class Meta:
        ordering = ('Id',)


class Notification(models.Model):
    Id = models.AutoField(primary_key=True)
    Type_Id = models.ForeignKey(NotificationType, on_delete=models.SET_DEFAULT, default=0)
    From_Id = models.IntegerField(default=0)
    To_Id = models.IntegerField(default=0)
    Status_Id = models.ForeignKey(NotificationStatus, on_delete=models.SET_DEFAULT, default=0)
    Message_Id = models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Notification"

    class Meta:
        ordering = ('Id',)


class UserLogin(models.Model):
    Id = models.AutoField(primary_key=True)
    User_Id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Login")
    Inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    Status_Id = models.ForeignKey(LoginStatus, on_delete=models.SET_DEFAULT, default=0)
    Attempts = models.IntegerField(default=0, blank=False, null=False)
    Updated = models.DateTimeField(auto_now_add=True, verbose_name="Time updated")
    IP_Address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP Address of Login")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "UserLogin"

    class Meta:
        ordering = ('Id',)


class PasswordReset(models.Model):
    Id = models.AutoField(primary_key=True)
    User_Id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=0)
    Authorization_Code = models.CharField(max_length=AUTHORIZATION_CODE_LENGTH,
                                          blank=False,
                                          verbose_name="Password Reset Code")
    Status_Id = models.ForeignKey(PasswordResetStatus, on_delete=models.SET_DEFAULT, default=0)
    Clicked = models.DateTimeField(auto_now=True, verbose_name="Time clicked")
    Inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Password Reset"

    class Meta:
        ordering = ('Id',)


class Name(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Name of User")
    User_Id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Login")
    Inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    Type_Id = models.ForeignKey(NameType, on_delete=models.SET_DEFAULT, default=0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Registered"

    class Meta:
        ordering = ('Id',)


class EmailAddress(models.Model):
    Id = models.AutoField(primary_key=True)
    Email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email of Register")
    User_Id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Login")
    Inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    Status_Id = models.ForeignKey(EmailAddressStatus, on_delete=models.SET_DEFAULT, default=0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % "Registered"

    class Meta:
        ordering = ('Id',)
