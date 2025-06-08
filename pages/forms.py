from django import forms
from accounts.models import BarberUser
from .models import Site

#Asosiy sayt malumotlari formasi<<<
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['sites_name', 'description', 'about', 'location', 'url1', 'url2', 'url3', 'tel',
                  'yt']

#Profil tahririlash form<<<
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = BarberUser
        fields = ['phone', 'first_name', 'last_name', 'profile_image']
        widgets = {
            'profile_image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['phone'].disabled = True
