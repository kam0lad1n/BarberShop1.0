from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse
from accounts.models import BarberUser
from config import settings


#Barber uchun model<<<
User = get_user_model()
class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    tajriba = models.IntegerField( null=True, blank=True)
    haqida = models.CharField(max_length=100, null=True, blank=True)
    yoshi = models.IntegerField( null=True, blank=True)
    rasmi = models.ImageField(upload_to='barber_image/', null=True, blank=True)

    def __str__(self):
        return str(self.user)

#Tarif uchun modeli<<<
class Level(models.Model):
    barber = models.ForeignKey(
        Barber, on_delete=models.CASCADE, related_name='levels'
    )
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=15, decimal_places=3)

    class Meta:
        unique_together = ('barber', 'name')

    def __str__(self):
        return f"{self.name} ({self.barber})"

#Sana uchun model<<<
class Date(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ('barber', 'date')

    def __str__(self):
        return f"{self.barber} | {self.date.strftime('%d.%m.%Y')}"

#Vaqt uchun model<<<
class Time(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='times', null=True)
    time = models.TimeField()

    class Meta:
        unique_together = ('barber', 'time')

    def __str__(self):
        return f" {self.barber} | {self.time.strftime('%H:%M')}"

#Mijoz uchun model<<<
class Client(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    ism = models.CharField(max_length=100, null=True)
    familiya = models.CharField(max_length=100, null=True, blank=True, default='')
    telefon = models.CharField(max_length=100, null=True)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, null=True, related_name='clients')
    sana = models.ForeignKey(Date, on_delete=models.CASCADE, null=True)
    vaqt = models.ForeignKey(Time, on_delete=models.CASCADE, null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_amount(self):
        return self.level.value if self.level else Decimal('0.000')

    def __str__(self):
        return f"{self.ism} "

    def get_absolute_url(self):
        return reverse('home', kwargs={'pk': self.pk})

#Balans uchun model<<<
class Balance(models.Model):
    user = models.ForeignKey(BarberUser, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=20, decimal_places=3)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} so'm - {self.date.strftime('%Y-%m-%d %H:%M')}"

#Admin Code uchun model<<<
class StaffCode(models.Model):
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.code

