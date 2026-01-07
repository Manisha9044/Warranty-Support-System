from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_customer', False)

        return self.create_user(email=email, password=password, first_name="Admin", last_name="User", user_type="Admin", **extra_fields)


class Custom_User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    profile_pic = models.FileField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user_type = models.CharField(max_length=200, choices=USER_TYPE_CHOICES, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
