from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models import CharField

# Create your models here.
class BarberUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


class BarberUser(AbstractUser):
    username = None
    phone = CharField(max_length=20, unique=True, verbose_name='Telefon raqami', blank=False)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    account_balance = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = BarberUserManager()
    def __str__(self):
        return self.first_name

