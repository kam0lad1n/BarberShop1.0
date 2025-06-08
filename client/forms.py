import datetime
from django import forms
from django.contrib.auth import get_user_model
from .models import Client, Level, Balance, Date, Time, StaffCode,Barber

User = get_user_model()
#Mijoz uchun form<<<
class ClientForm(forms.ModelForm):
    barber = forms.ModelChoiceField(
        queryset=Barber.objects.all(),
        empty_label="Barber tanlash"
    )
    level = forms.ModelChoiceField(
        queryset=Level.objects.all(),
        empty_label="Level tanlang",
        required=True
    )

    class Meta:
        model = Client
        fields = ['ism', 'familiya', 'telefon', 'barber', 'sana', 'vaqt', 'level']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['level'].queryset = Level.objects.all()

            self.fields['barber'].queryset = User.objects.filter(is_staff=True)

    def save(self, commit=True, barber_user=None):
        instance = super().save(commit=False)
        if not barber_user:
            raise ValueError("Barber user majburiy bo'lishi kerak")
        instance.owner = barber_user  # owner sifatida barberning useri
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        barber = cleaned_data.get('barber')
        sana = cleaned_data.get('sana')
        vaqt = cleaned_data.get('vaqt')

        if barber and sana and vaqt:
            if Client.objects.filter(barber=barber, sana=sana, vaqt=vaqt).exists():
                raise forms.ValidationError("Bu vaqt allaqachon band qilingan, boshqa vaqtni tanlang!")
        return cleaned_data

#Barber uchun form<<<
class BarberForm(forms.ModelForm):
    sana = forms.DateField(
        label='Sana',
        required=True,
        input_formats=['%d-%m-%Y']
    )

    class Meta:
        model = Client
        fields = ['ism', 'familiya', 'telefon', 'sana', 'vaqt']

    def __init__(self, *args, **kwargs):
        self.barber = kwargs.pop('barber', None)
        super().__init__(*args, **kwargs)

        today = datetime.date.today()
        dates = [(today + datetime.timedelta(days=i)).strftime('%d-%m-%Y') for i in range(7)]
        self.fields['sana'].widget = forms.Select(choices=[('', "Sanani tanlang..")] + [(d, d) for d in dates])

        times = [f"{h:02}:00" for h in range(8, 24)]
        self.fields['vaqt'].widget = forms.Select(choices=[('', "Vaqtni tanlang..")] + [(t, t) for t in times])

    def clean(self):
        cleaned_data = super().clean()
        sana = cleaned_data.get('sana')
        vaqt = cleaned_data.get('vaqt')

        if sana and vaqt:
            if Client.objects.filter(barber=self.barber, sana=sana, vaqt=vaqt).exists():
                raise forms.ValidationError('Bu vaqt bu barber uchun band qilingan!')
        return cleaned_data

#Tartiblash uchun form<<<
class OrderForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['vaqt']
        widgets = {
            'vaqt': forms.TimeInput(attrs={'type': 'vaqt', 'step': '60', 'value': '24:00'}),
        }

    def clean_time(self):
        """ 24 soatlik formatni ta’minlash """
        time = self.cleaned_data['vaqt']
        return time.strftime("%H:%M")

#Balance uchun form<<<
class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': "Yechmoqchi bo‘lgan summani kiriting"})
        }

#StaffCode uchun form<<<
class StaffCodeForm(forms.ModelForm):
    class Meta:
        model = StaffCode
        fields = ['code']

#Tarif uchun form<<<
class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ['name', 'value']
#Sana uchun form<<<
class DateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.barber = kwargs.pop('barber', None)
        super().__init__(*args, **kwargs)

        today = datetime.date.today()
        date_choices = [
            (today + datetime.timedelta(days=i), (today + datetime.timedelta(days=i)).strftime('%d-%m-%Y'))
            for i in range(30)
        ]

        selected_dates = set()
        if self.barber:
            selected_dates = set(
                Date.objects.filter(barber=self.barber).values_list('date', flat=True)
            )

        for date_value, date_label in date_choices:
            self.fields[f'date_{date_value}'] = forms.BooleanField(
                label=date_label,
                required=False,
                initial=(date_value in selected_dates)
            )
#Vaqt uchun form<<<
class TimeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.barber = kwargs.pop('barber', None)
        self.step_minutes = kwargs.pop('step', 60)  # Default 30 daqiqa
        super().__init__(*args, **kwargs)
        selected_times = set()
        if self.barber:
            selected_times = set(
                Time.objects.filter(barber=self.barber).values_list('time', flat=True)
            )

        current = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0))
        end = datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59))

        while current <= end:
            time_label = current.strftime('%H:%M')
            field_name = f'time_{time_label}'
            self.fields[field_name] = forms.BooleanField(
                label=time_label,
                required=False,
                initial=(current.time() in selected_times)
            )
            current += datetime.timedelta(minutes=self.step_minutes)