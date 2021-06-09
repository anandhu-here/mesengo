from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
# from blissedmaths.utils import unique_otp_generator
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


    

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None,  is_staff=False, is_active=True, is_admin=False):
        if not email:
            raise ValueError('users must have a valid email')

        user_obj = self.model(
            email=email
        )
        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,first_name, last_name, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True, 
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user


class User(AbstractBaseUser):
    first_name  = models.CharField(blank = True,max_length=200, null = True)
    last_name   = models.CharField(blank = True, null = True, max_length=200)
    email       = models.EmailField(blank=False, null=False, unique=True)
    standard    = models.CharField(max_length = 3, blank = True, null = True)
    score       = models.IntegerField(default = 16)
    first_login = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.first_name)

    def get_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def get_short_name(self):
        return str(self.first_name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
   





def get_filename_ext(filename, obj):
    return f"profile/{obj.user.name}/{filename}"





class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    # logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    # forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    # forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)
