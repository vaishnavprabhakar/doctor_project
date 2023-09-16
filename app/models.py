from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from app.validators import validate_username
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    

    
class DoctorDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hospital = models.CharField(verbose_name='Hospital Name', null=True, )
    specialization = models.CharField(null=True)



@receiver(post_save,sender=CustomUser)
def doctor_post_save_receiver(sender, created, instance, *args, **kwargs):
    if created and instance.is_doctor:
        DoctorDetails.objects.create(user=instance)