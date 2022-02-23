from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser
    )
from django.conf import settings
from PIL import Image
from uuid import uuid4
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """User model"""
    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
        
    def get_name(self):
        return super().get_full_name()
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(default='user.png', upload_to='profile_pics')
    description = models.CharField(max_length=25)
    status = models.CharField(max_length=25)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " 's Profile"
    
    def save(self, *args, **kwargs):
        img = Image.open(self.profile_picture)

        if img.height > 300 or img.width > 300:
            output = BytesIO()
            current_file_ext = self.profile_picture.name.split('.')[-1]
            ext = ''
            if current_file_ext == 'jpg' or current_file_ext == 'jfif':
                ext = 'JPEG'
            else:
                ext = current_file_ext
            img = img.resize((300, 300))

            img.save(output, format='{}'.format(ext).upper(), quality=100)
            output.seek(0)

            the_hex = uuid4().hex
            self.profile_picture = InMemoryUploadedFile(output, "ImageField",
                f'{the_hex}.jpg', 'image/jpeg',
                sys.getsizeof(output), None)

        super().save(*args, **kwargs)
        
