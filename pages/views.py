from django import template
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from client.models import Barber
from pages.forms import ProfileEditForm, SiteForm
from pages.models import Site


# Create your views here.


#Base htmlni o'qish uchun
def base_view(request):
    site = Site.objects.first()
    return render(request, 'base.html', {'site': site})

#HomePageni o'qish uchun<<<
def home_view(request):
    barbers = Barber.objects.all()
    site = Site.objects.first()
    return render(request, 'pages/home.html', {'barbers': barbers, 'site': site})

#Sayt malumotlarini yangilash uchun
def site_update(request):
    site = Site.objects.first()
    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('home')  #
    else:
        form = SiteForm(instance=site)

    return render(request, 'pages/site_edit.html', {'form': form})

#Adminlik boshqaruvi uchun<<<
def admin_view(request):
    return

#Profilni o'qish uchun
@login_required
def profile_view(request):
    user = request.user
    return render(request, 'pages/profile.html', {"user": user})

#Profilni tahrirlash uchun<<<
@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'pages/profile_edit.html', {'form': form, 'user': user})


#Userlarni o'qish uchun<<<
User = get_user_model()
@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'barbers/users.html', {'users': users})
#Userlarni o'chirish uchun<<<
@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user != request.user:
            user.delete()
            messages.success(request, "Foydalanuvchi o‘chirildi.")
        else:
            messages.error(request, "O‘zingizni o‘chira olmaysiz.")
    return redirect('users_list')

#Admin qilish uchun<<<
@login_required
@user_passes_test(lambda u: u.is_superuser)
def make_admin(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        user.is_staff = True
        user.save()
        messages.success(request, f"{user.first_name} admin qilib belgilandi!")
    else:
        messages.error(request, "Faqat superadminlar foydalanuvchini admin qila oladi!")
    return redirect('users_list')


#Oddiy User qilish uchun<<<
@login_required
@user_passes_test(lambda u: u.is_superuser)
def remove_admin(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        if user != request.user:
            user.is_superuser = False
            user.is_staff = False
            user.save()
            messages.success(request, f"{user.first_name} endi oddiy foydalanuvchi bo‘ldi!")
        else:
            messages.error(request, "O‘zingizning adminligingizni olib tashlay olmaysiz!")
    else:
        messages.error(request, "Faqat superadminlar foydalanuvchini oddiy user qila oladi!")
    return redirect('users_list')

