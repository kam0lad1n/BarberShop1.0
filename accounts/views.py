from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import FormView

from client.models import StaffCode
from sms.sms import send_sms
from .forms import *


#Ro'yxatdan o'tish uchun<<<
class BarberRegisterView(View):
    success_url = reverse_lazy('login')

    def get(self, request):
        form = BarberRegisterForm()
        return render(request, 'registration/register.html', {"form": form})

    def post(self, request):
        if request.method == "POST":
            form = BarberRegisterForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                if form.cleaned_data.get('is_staff_code_used') and form.cleaned_data.get('staff_code'):
                    code = form.cleaned_data['staff_code']
                    if StaffCode.objects.filter(code=code).exists():
                        user.is_staff = True
                user.set_password(form.cleaned_data['password1'])
                user.save()
                return redirect(self.success_url)
            else:
                print(form.errors)
        else:
            form = BarberRegisterForm()

        return render(request, 'registration/register.html', {'form': form})

#Login qilish uchun<<<
class BarberLoginView(LoginView):
    form_class = BarberLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')


#Parolni o'zgartirish uchun<<<
class BarberPasswordChangeView(PasswordChangeView, LoginRequiredMixin):
    # form_class = BarberPasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('change_password_done')

def reset_password_done(request):
    return  render(request, "registration/change_password_done.html")


#Parolni tiklash uchun<<<
User = get_user_model()


def send_password_reset_link(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_url = request.build_absolute_uri(
        reverse('reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
    )

    sms_text = f"Sizning parolni tiklash havolangiz: {reset_url}"
    print(sms_text)
    phone = user.phone
    print(phone)
    send_sms(phone, sms_text)  # yoki user.telefon agar maydon nomi shunday bo‘lsa
def custom_password_reset(request):
    if request.method == 'POST':
        form = BarberPasswordResetForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            try:
                user = User.objects.get(phone=phone)
                send_password_reset_link(user,request)
                return redirect('reset_password_done')
            except User.DoesNotExist:
                form.add_error('phone', 'Bunday telefon raqamli foydalanuvchi topilmadi.')
            except User.MultipleObjectsReturned:
                form.add_error('phone', 'Bu telefon raqam bir nechta foydalanuvchiga tegishli.')

    else:
        form = BarberPasswordResetForm()
    return render(request, 'registration/reset_password.html', {'form': form})

#Parol tiklash havola yuborilganligi<<<
class BarberPasswordResetDone(PasswordResetDoneView, LoginRequiredMixin):
    template_name = 'registration/reset_password_done.html'
    success_url = 'home'

#Parolni tiklashni tasdiqlash uchun<<<
class BarberPasswordResetConfirmView(PasswordResetConfirmView, LoginRequiredMixin):
    template_name = 'registration/reset_password_confirm.html'
    success_url = 'login'

def barberpasswordresetconfirmdone(request):
    return render(request, 'registration/reset_password_confirm_done.html')