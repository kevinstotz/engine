from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
from random import randint, choice
import string
import time
from SES.settings.base import \
    EMAIL_SERVER, \
    EMAIL_TEMPLATE_DIR, \
    NOTIFICATION_STATUS, \
    EMAIL_FROM_DOMAIN, \
    EMAIL_TEMPLATE, \
    EMAIL_LOGIN_URL, \
    NOTIFICATION_TYPE, \
    EMAIL_VERIFY_ACCOUNT_URL, \
    EMAIL_VERIFY_TRACK_URL, \
    EMAIL_ADDRESS_STATUS, \
    PASSWORD_RESET_URL, \
    PASSWORD_RESET_STATUS, \
    PASSWORD_LENGTH, \
    NAME_TYPE, \
    REGISTER_STATUS
from SES.models import \
    EmailTemplate, \
    Notification, \
    NotificationType, \
    NotificationStatus, \
    NameType, \
    Name, \
    CustomUser, \
    EmailAddress, \
    EmailAddressStatus, \
    PasswordResetStatus, \
    PasswordReset
from SES.models import Register, RegisterStatus
from SES.classes.utils import ReturnResponse
from os.path import join
import logging

logger = logging.getLogger(__name__)


class MyEmail:

    # class variable shared by all instances
    emailHost = ""
    emailPort = 0
    emailPassword = EMAIL_SERVER['PASSWORD']
    emailUsername = EMAIL_SERVER['USER']

    def __init__(self, name):
        #  instance variable unique to each instance
        self.name = name
        self.emailTemplate = ""
        self.subject = ""
        self.body = ""
        self.toEmail = ""
        self.fromEmail = ""

    def replace_string_in_template(self, search, replace):
        logger.debug('Searched:{0} Replaced:{1}'.format(search, replace))
        self.body = self.body.replace(search, replace)

    def load_template(self, template_filename):

        filename = join(EMAIL_TEMPLATE_DIR, template_filename)
        with open(filename, "rt") as template:
            self.body = template.read()

        if len(self.body) > 10:
            result = 'Read Email Template:{0}'.format(filename)
            logger.debug(result)
            return ReturnResponse.Response(0, __name__, 'success', result).return_json()
        else:
            result = 'Failed Reading Email Template:{0}'.format(filename)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

    def send_verify_email(self, register_id):

        try:
            register_user = Register.objects.get(pk=register_id)
            result = 'Retrieved register id:{0}'.format(register_id)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed getting register id:{0}'.format(register_id)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['VERIFY'])
            result = 'Getting EMAIL_TEMPLATE VERIFY :{0} from DB:'.format(email_template.HTML_Filename)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed getting EMAIL_TEMPLATE record #:{0} from DB:'.format(EMAIL_TEMPLATE['VERIFY'])
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        notification = Notification()
        notification.To_Id = register_user.pk
        notification.Message_Id = email_template.pk
        notification.Type_Id = NotificationType(pk=NOTIFICATION_TYPE['EMAIL'])

        try:
            self.load_template(email_template.HTML_Filename.name)
            result = 'read email template file:{0}'.format(email_template.HTML_Filename.name)
            logger.debug(result)
        except:
            result = 'Failed reading email template:{0}'.format(email_template.HTML_Filename.name)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.subject = email_template.Subject
        self.fromEmail = email_template.From + '@' + EMAIL_FROM_DOMAIN
        self.toEmail = register_user.Email
        self.replace_string_in_template('EMAIL_VERIFY_TRACK_URL',
                                        EMAIL_VERIFY_TRACK_URL + register_user.Authorization_Code)
        self.replace_string_in_template('EMAIL_VERIFY_ACCOUNT_URL',
                                        EMAIL_VERIFY_ACCOUNT_URL + register_user.Authorization_Code)
        self.replace_string_in_template('FIRST_NAME', register_user.First_Name + " ")
        self.replace_string_in_template('LAST_NAME', register_user.Last_Name)

        if self.send() == 1:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            register_user.Status_Id = RegisterStatus.objects.get(pk=REGISTER_STATUS['SENT'])
            register_user.save()
            result = 'Registered User and sent email to user ID:{0}'.format(register_user.Status_Id)
            logger.debug(result)
        else:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed sending email:{0} to user ID:{1}'.format(email_template.HTML_Filename.name,
                                                                      register_user.Status_Id)
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()
        notification.save()
        result = 'Verify email sent to:{}'.format(self.toEmail)
        return ReturnResponse.Response(0, __name__, 'success', result).return_json()

    def send_welcome_email(self, new_user, new_password):

        try:
            new_user = CustomUser.objects.get(pk=new_user.pk)
            result = 'Loaded New User in Users: Id:{0}'.format(new_user.pk)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Could not find New User in Users: Id:{0}'.format(new_user.pk)
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['WELCOME'])
            result = 'Loaded Email Template WELCOME:{0}'.format(email_template.HTML_Filename.name)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Could not find New User in Users: Id:{0}'.format(new_user.pk)
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        notification = Notification()
        notification.To_Id = new_user.pk
        notification.Message_Id = email_template.pk

        try:
            notification.Type_Id = NotificationType.objects.get(pk=NOTIFICATION_TYPE['EMAIL'])
            result = 'Loaded email type notification: Id:{0}'.format(NOTIFICATION_TYPE['EMAIL'])
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed loading email type notification: Id:{0}'.format(NOTIFICATION_TYPE['EMAIL'])
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        try:
            self.load_template(email_template.HTML_Filename.name)
            result = 'read email template file:{0}'.format(email_template.HTML_Filename.name)
            logger.debug(result)
        except:
            result = 'Failed reading email template:{0}'.format(email_template.HTML_Filename.name)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.subject = email_template.Subject
        self.fromEmail = email_template.From + '@' + EMAIL_FROM_DOMAIN

        try:
            email_address_status = EmailAddressStatus.objects.get(pk=EMAIL_ADDRESS_STATUS['ACTIVE'])
            result = 'Loaded email address status Active: Id:{0}'.format(EMAIL_ADDRESS_STATUS['ACTIVE'])
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading email address status Active: Id:{0}'.format(EMAIL_ADDRESS_STATUS['ACTIVE'])
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        try:
            email_address = EmailAddress.objects.get(User_Id=new_user, Status_Id=email_address_status)
            result = 'Loaded email address :{0}'.format(email_address.Email)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading email address:'
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()
        self.toEmail = email_address.Email

        try:
            name_type = NameType.objects.get(pk=NAME_TYPE['FIRST'])
            result = 'Loaded name type:{0}'.format(name_type.Type)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading Name Type First:'
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        try:
            name = Name.objects.get(User_Id=new_user, Type_Id=name_type)
            result = 'Loaded name:{0}'.format(name.Name)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading Name:'
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.subject = self.subject.replace('NAME', name.Name)
        self.replace_string_in_template('PASSWORD', str(new_password))
        self.replace_string_in_template('USERNAME', email_address.Email)
        self.replace_string_in_template('FIRST_NAME', name.Name)

        if self.send() == 1:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            result = 'Welcome Email Sent to:{0}'.format(email_address.Email)
            logger.debug(result)
        else:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed Welcome Email Sent to:{0}'.format(email_address.Email)
            logger.info(result)
        notification.save()
        return ReturnResponse.Response(0, __name__, 'success', result).return_json()

    def send_forgot_password_email(self, user):

        try:
            password_reset = PasswordReset.objects.get(User_Id=user, Status_Id=PASSWORD_RESET_STATUS['ACTIVE'])
            result = 'Loaded password reset for user Id:{0}'.format(user.pk)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading password reset for user Id:{0}'.format(user.pk)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        password_reset.Clicked = time.time()
        password_reset.save()

        if password_reset.Status_Id == PASSWORD_RESET_STATUS['EXPIRED']:
            result = 'This Request has expired!  Click forgot password again.'
            logger.debug(result)
            return ReturnResponse.Response(0, __name__, 'success', result).return_json()

        if (password_reset.Clicked - password_reset.Inserted) > timedelta(1):
            password_reset.Status_Id = PasswordResetStatus(pk=PASSWORD_RESET_STATUS['EXPIRED'])
            password_reset.save()
            result = 'This Request has expired!  Click forgot password again.'
            logger.debug(result)
            return ReturnResponse.Response(0, __name__, 'success', result).return_json()

        if password_reset.Status_Id == PASSWORD_RESET_STATUS['CLICKED']:
            result = 'This Request has already been used!  Click forgot password again.'
            logger.debug(result)
            return ReturnResponse.Response(0, __name__, 'success', result).return_json()

        if password_reset.Status_Id == PASSWORD_RESET_STATUS['ACTIVE']:
            password_reset.Status_Id = PasswordResetStatus(pk=PASSWORD_RESET_STATUS['CLICKED'])
            password_reset.save()

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['FORGOT'])
            result = 'Loaded email template FORGOT:{0}'.format(email_template.HTML_Filename.name)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading email template FORGOT ID{0}:'.format(EMAIL_TEMPLATE['FORGOT'])
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        notification = Notification()
        notification.To_Id = user.pk
        notification.Message_Id = email_template.pk

        try:
            notification.Type_Id = NotificationType.objects.get(pk=NOTIFICATION_TYPE['EMAIL'])
            result = 'Loaded Notification type EMAIL:{0}'.format(NOTIFICATION_TYPE['EMAIL'])
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading Notification type EMAIL:{0}'.format(NOTIFICATION_TYPE['EMAIL'])
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        try:
            self.load_template(email_template.HTML_Filename.name)
            result = 'read email template file:{0}'.format(email_template.HTML_Filename.name)
            logger.debug(result)
        except:
            result = 'Failed reading email template:{0}'.format(email_template.HTML_Filename.name)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.subject = email_template.Subject
        self.fromEmail = email_template.From + '@' + EMAIL_FROM_DOMAIN
        self.toEmail = user.Email

        try:
            name = Name.objects.get(User_Id=user, Type_Id=NameType.objects.get(pk=NAME_TYPE['FIRST']))
            first_name = name.Name
            result = 'Read User from DB:{0}'.format(first_name)
            logger.debug(result)
        except ObjectDoesNotExist:
            first_name = ""
            result = 'Failed reading user first name from DB UserId:{0}'.format(user.pk)
            logger.critical(result)

        self.subject = self.subject.replace('NAME', first_name)
        self.replace_string_in_template('PASSWORD_RESET_URL', PASSWORD_RESET_URL + password_reset.Authorization_Code)

        if self.send() == 1:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            result = 'Forgot Password Email Sent to:{0}'.format(user.Email)
            logger.debug(result)
        else:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed sending Forgot Password Email to:{0}'.format(user.Email)
            logger.error(result)
        notification.save()
        return ReturnResponse.Response(0, __name__, 'success', result).return_json()

    def send_reset_password_email(self, authorization_code):

        try:
            password_reset = PasswordReset.objects.get(Authorization_Code=authorization_code)
            result = 'Read authorization code from DB:{0}'.format(authorization_code)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Finding Authorization Code in Password Reset:{0}'.format(authorization_code)
            logger.info(result)
            return ReturnResponse.Response(0, __name__, 'failed', result).return_json()

        if authorization_code != password_reset.Authorization_Code:
            result = 'Codes do not match.  Request password again.:{0}<>{1}'.format(authorization_code,
                                                                                    password_reset.Authorization_Code)
            logger.info(result)
            return ReturnResponse.Response(0, __name__, 'failed', result).return_json()

        if password_reset.Status_Id.pk == PASSWORD_RESET_STATUS['FINISHED']:
            result = 'Already Used this request.  Request password again. ID:{0}'.format(password_reset.Status_Id.pk)
            logger.info(result)
            return ReturnResponse.Response(0, __name__, 'failed', result).return_json()

        password_reset.Clicked = time.time()
        password_reset.Status_Id = PasswordResetStatus.objects.get(pk=PASSWORD_RESET_STATUS['FINISHED'])
        password_reset.save()

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['RESET'])
            result = 'retrieve email template file:{0}'.format(email_template.HTML_Filename.name)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed retrieving email RESET template:{0}'.format(EMAIL_TEMPLATE['RESET'])
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        notification = Notification()
        notification.To_Id = password_reset.User_Id.pk
        notification.Message_Id = email_template.pk
        notification.Type_Id = NotificationType.objects.get(pk=NOTIFICATION_TYPE['EMAIL'])

        try:
            self.load_template(email_template.HTML_Filename.name)
            result = 'read email template file:{0}'.format(email_template.HTML_Filename.name)
            logger.debug(result)
        except:
            result = 'Failed reading email template:{0}'.format(email_template.HTML_Filename.name)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.subject = email_template.Subject
        self.fromEmail = email_template.From + '@' + EMAIL_FROM_DOMAIN

        try:
            user = CustomUser.objects.get(Id=password_reset.User_Id.pk)
            result = 'Read email address from user:{0}'.format(user.Email)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed reading user email address from User ID:{0}'.format(password_reset.User_Id)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.toEmail = user.Email

        try:
            name = Name.objects.get(User_Id=user.Id, Type_Id=NameType.objects.get(pk=NAME_TYPE['FIRST']))
            first_name = name.Name
            result = 'Read user id and first name from password reset:{0}'.format(name.Id)
            logger.debug(result)
        except ObjectDoesNotExist:
            first_name = ""
            result = 'Failed reading user id and first name from password reset:{0}'.format(user.Id)
            logger.error(result)

        new_password = self.generate_password()
        user.set_password(new_password)
        user.save()
        self.replace_string_in_template('NEW_PASSWORD', str(new_password))
        self.subject = self.subject.replace('NAME', first_name)
        self.replace_string_in_template('EMAIL_LOGIN_URL', str(EMAIL_LOGIN_URL))
        if self.send() == 1:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            result = 'Reset Password Email Sent to:{0}'.format(user.Email)
            logger.debug(result)
        else:
            notification.Status_Id = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed sending Reset Password Email to:{0}'.format(user.Email)
            logger.error(result)
        notification.save()
        return ReturnResponse.Response(0, __name__, 'success', result).return_json()

    def generate_password(self):
        letters = string.ascii_lowercase
        new_password = ''.join(choice(letters) for i in range(PASSWORD_LENGTH))
        result = 'Generated new Password:{0}'.format(new_password)
        logger.debug(result)
        return new_password

    def send(self):
        return send_mail(
            self.subject,
            "txt version",
            self.fromEmail,
            [self.toEmail],
            html_message=self.body,
            auth_user=self.emailUsername,
            auth_password=self.emailPassword,
            fail_silently=False)
