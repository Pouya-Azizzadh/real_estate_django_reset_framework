# users/models.py
import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('ایمیل الزامی است')
        if not phone_number:
            raise ValueError('شماره تلفن الزامی است')
        if not password:
            raise ValueError('وارد کردن رمز الزامی است')
        email = self.normalize_email(email) if email else None
 
        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)
    


def validate_unique_positive_integer(value):
    if value != 1 and CustomUser.objects.filter(national_code=value).exists():
        raise ValidationError('کد ملی تکراری است')
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    image_profile=models.ImageField(null=True,blank=True,upload_to='images/')
    username=models.CharField(max_length=30,default='',blank=True)
    first_name = models.CharField(max_length=30,default='',blank=True)
    last_name = models.CharField(max_length=30,default='',blank=True)
    code = models.CharField(max_length=6,blank=False,default='')
    email = models.EmailField(unique=True, null=True, blank=True)
    national_code=models.CharField(max_length=10,unique=True,null=True, blank=True)
    phone_number = models.CharField( max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number','national_code','image_profile']

     
    def __str__(self):
        return self.email or self.phone_number

    def get_full_name(self):
        return self.email or self.phone_number

    def get_short_name(self):
        return self.email or self.phone_number