from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from app.validators import validate_username


class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30,null=True)
    username = models.CharField(max_length=30, null=True, validators=[validate_username])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_doctor = models.BooleanField(null=True, default=False)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    def __str__(self):
        return self.email
    
    
