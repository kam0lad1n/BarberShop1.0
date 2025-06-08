from tkinter.font import names

from django.urls import path
from .views import *


urlpatterns = [

    path('signup/', BarberRegisterView.as_view(), name='register'),
    path('login/', BarberLoginView.as_view(), name='login'),
    path('password_change/', BarberPasswordChangeView.as_view(), name='change_password'),
    path('password_change/done/', reset_password_done, name='change_password_done'),
    path('password_reset/', custom_password_reset, name='reset_password'),
    path('password_reset/done/', BarberPasswordResetDone.as_view(), name='reset_password_done'),
    path('password_reset/<uidb64>/<token>/', BarberPasswordResetConfirmView.as_view(),
         name='reset_password_confirm'),
    path('password_reset/confirm/done/', barberpasswordresetconfirmdone, name='reset_password_confirm_done')
]
