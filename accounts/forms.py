from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from client.models import StaffCode
from .models import BarberUser
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm


class BarberRegisterForm(UserCreationForm):
    is_staff_code_used = forms.BooleanField(required=False, label="Staffmanmisiz?")
    staff_code = forms.CharField(required=False, label="Staff kodi")

    class Meta:
        model = BarberUser
        fields = ('phone', 'first_name', 'last_name', 'profile_image')

    def clean(self):
        cleaned_data = super().clean()
        code_checked = cleaned_data.get('is_staff_code_used')
        code_input = cleaned_data.get('staff_code')

        if code_checked and code_input:
            if not StaffCode.objects.filter(code=code_input).exists():
                raise forms.ValidationError("Staff kodi noto‘g‘ri.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Parol'
        self.fields['password2'].label = 'Parolni tasdiqlang'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = False
        self.fields['profile_image'].required = False
        self.fields['staff_code'].required = False


class BarberLoginForm(AuthenticationForm):
    username = forms.CharField(label="Telefon raqam",
                               widget=forms.TextInput(attrs={'placeholder': 'Telefon raqamingiz'}))
    password = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={'placeholder': 'Parolingiz'}))
    error_messages = {
        'invalid_login': _("Telefon raqami yoki parol noto‘g‘ri. Iltimos, qaytadan urinib ko‘ring."),
        'inactive': _("Bu foydalanuvchi akkaunti o‘chirilgan."),
    }



class BarberPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Eski parol",
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Eski parolingiz'}))
    new_password1 = forms.CharField(label="Yangi parol",
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parol'}))
    new_password2 = forms.CharField(label="Yangi parolni tasdiqlang",
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parolni tasdiqlang'}))


class BarberPasswordResetForm(forms.Form):
    phone = forms.CharField(
        label="Telefon raqam",
        error_messages={"invalid": "Telefon raqamni to‘g‘ri kiriting (masalan: +998901234567)"},
        widget=forms.TextInput(attrs={
            'placeholder': '+998901234567',
            'type': 'tel'
        })
    )


class BarberSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Yangi parol",
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parol'}))
    new_password2 = forms.CharField(label="Yangi parolni tasdiqlang",
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parolni tasdiqlang'}))
