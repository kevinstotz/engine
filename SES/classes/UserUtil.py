from SES.models import CustomUser
from random import randint
from django.core.exceptions import ObjectDoesNotExist

class Util:

    def __init__(self):
        #  instance variable unique to each instance
        self.new_username = ""
        self.num_records = 1

    def find_username(self, username):

        while True:
            self.new_username = username + '_' + str(randint(100, 999))
            try:
                self.num_records = CustomUser.objects.get(Username=username).count()
            except ObjectDoesNotExist:
                self.num_records = 0
                break

        return self.num_records
