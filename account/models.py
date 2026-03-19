from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, password, **extra_fields)
    
class User(AbstractUser):

    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('area_officer', 'Area Officer'),
    )

    username = None   # remove username login

    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True,validators=[EmailValidator])
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    # def __str__(self):
    #     return str(self.user_id)
    
class Citizen(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    aadhar = models.CharField(max_length=12, unique=True)
    account_status = models.CharField(max_length=20, default="active")

    def __str__(self):
        return f"Citizen - {self.user.full_name}"

class AreaOfficer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    badge_number = models.CharField(max_length=50, unique=True)
    assigned_area = models.CharField(max_length=150)

    def __str__(self):
        return f"Officer - {self.user.full_name}"

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.full_name} Contact"
    

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} Profile"