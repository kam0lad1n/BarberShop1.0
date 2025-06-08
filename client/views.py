import logging
import threading
import datetime
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, View, CreateView
from django.views.generic.edit import DeleteView
from sms.sms import send_sms
from .forms import ClientForm, LevelForm, BalanceForm, DateForm, TimeForm
from .models import Client, Level, Date, Time, Balance, StaffCode, Barber

class BarberRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            self.barber = Barber.objects.get(user=request.user)
        except Barber.DoesNotExist:
            return redirect('not_barber')
        return super().dispatch(request, *args, **kwargs)

# Bandlik yaratish<<<
@login_required
def booking_view(request):
    barbers = Barber.objects.all()
    selected_barber_id = request.GET.get('barber_id') or request.POST.get('barber')

    days = Date.objects.none()
    times = Time.objects.none()
    levels = Level.objects.none()
    if selected_barber_id:
        try:
            barber = Barber.objects.get(id=selected_barber_id)
            user_id = barber.id
            days = Date.objects.filter(barber_id=user_id)
            times = Time.objects.filter(barber_id=user_id)
            levels = Level.objects.filter(barber_id=user_id)
        except Barber.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            barber = Barber.objects.get(id=request.POST.get('barber'))
            booking = form.save(commit=False, barber_user=barber.user)  # owner sifatida barber.user
            booking.barber = barber
            booking.owner = request.user
            booking.save()
            # yaratiliganda
            phone = str(booking.telefon)
            phone = phone.replace(" ", "")
            phone = phone.replace("-", "")
            name = booking.ism
            tm = f"{booking.sana.date.strftime('%B %d, %Y')} sanasi, {booking.vaqt.time.strftime('%H:%M')}"
            text = f"Salom {name}\nSiz BarberShopdan joy band qildingiz.\nNavbatingiz:{tm} da.\nRaxmat )"
            print(text)
            send_sms(phone, text)

            # rejalashtirish 2soat oldn
            date_obj = booking.sana.date
            time_obj = booking.vaqt.time
            booking_datetime = datetime.combine(date_obj, time_obj)
            reminder_datetime = booking_datetime - timedelta(hours=2)
            print("Band qilingan vaqt:", booking_datetime)
            print("SMS yuboriladigan vaqt:", reminder_datetime)

            def schedule_sms(phone, text, send_time):
                delay = (send_time - datetime.now()).total_seconds()
                if delay > 0:
                    threading.Timer(delay, send_sms, args=[phone, text]).start()
                else:
                    print("SMS yuborish vaqti o‘tib ketgan.")

            sms_text = f"Hurmatli mijoz!\n{tm}ga band qilgan joyingizni unutmang!\nNavbatingiz kelishiga atiga 2soat qoldi."
            schedule_sms(phone, sms_text, reminder_datetime)

            return redirect('home')

    else:
        form = ClientForm()

    context = {
        'barbers': barbers,
        'days': days,
        'times': times,
        'levels': levels,
        'form': form,
        'selected_barber_id': selected_barber_id,
    }

    return render(request, 'bookings/new_booking.html', context)

def client_add_done(request):
    booking = Client.objects.first()
    return  render(request, "bookings/new_booking_done.html", {"booking": booking})

# Band qilingan joylar listi<<<
class ClientsListView(ListView, LoginRequiredMixin):
    model = Client
    template_name = 'bookings/bookings.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Client.objects.all().order_by('sana', 'vaqt')

        elif hasattr(user, 'barber'):
            return Client.objects.filter(barber=user.barber).order_by('sana', 'vaqt')
        else:
            return Client.objects.filter(owner=user).order_by('sana', 'vaqt')



class OnlyClientsRead(ListView, LoginRequiredMixin):
    model = Client
    template_name = 'bookings/bookings_view.html'
    context_object_name = 'clients_only'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Client.objects.all().order_by('sana', 'vaqt')

        elif hasattr(user, 'barber'):
            return Client.objects.filter(barber=user.barber).order_by('sana', 'vaqt')

        else:
            return Client.objects.filter(owner=user).order_by('sana', 'vaqt')



# Band qilingan joylarni o'chirish<<<
class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'bookings/delete_booking.html'
    success_url = reverse_lazy('clients')

    def test_func(self):
        obj = self.get_object()
        admin = self.request.user.is_superuser or self.request.user.is_staff
        owner = obj.owner == self.request.user
        return admin or owner

    def get(self, request, *args, **kwargs):
        """ GET so‘rovni bloklab, faqat POST orqali o‘chirishga ruxsat beramiz """
        return self.post(request, *args, **kwargs)




# Band qilingan joyni tugatish va balans qo'shish<<<
logger = logging.getLogger(__name__)
def complete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        logger.debug(f"Client: {client}, Owner: {client.owner}, Level: {client.level}")
        client.status = 'completed'
        client.save()
        if client.owner:
            amount = client.calculate_amount()
            if amount is None:
                return JsonResponse({'status': 'error', 'message': 'Hisoblangan qiymat noto‘g‘ri.'})
            client.owner.account_balance += amount
            client.owner.save()
        client.delete()
        return redirect('clients')

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

#Barber yaratish va boshqarish<<<
class BarberCreateView(CreateView):
    model = Barber
    fields = '__all__'
    template_name = 'barbers/add_barber.html'
    success_url = reverse_lazy('add_barber')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_users = User.objects.filter(is_staff=True)
        barber_users = Barber.objects.values_list('user_id', flat=True)
        available_users = staff_users.exclude(id__in=barber_users)

        context['users'] = available_users
        context['barbers'] = Barber.objects.all()
        return context

#No barber
def not_barber(request):
    return render(request, 'barbers/not_barber.html')

#Barberni o'chirish<<<
class DeleteBarbers(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Barber
    success_url = reverse_lazy('add_barber')
    template_name = 'barbers/delete_barber.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        barber = self.get_object()
        user = barber.user
        if user.id != request.user.id:
            Level.objects.filter(barber=user).delete()
            Date.objects.filter(barber=user).delete()
            Time.objects.filter(barber=user).delete()

            if request.user != user:
                user.is_staff = False
                user.is_superuser = False
                user.save()
            super().delete(request, *args, **kwargs)

        return redirect(self.success_url)


# Sana va Vaqt malumotlarini olish<<<
def get_data_for_barber(request):
    barber_id = request.GET.get('barber_id')
    response = {}

    if barber_id:
        date_objs = Date.objects.filter(barber_id=barber_id)
        dates = [{'id': obj.id, 'date': obj.date.strftime('%Y-%m-%d')} for obj in date_objs]
        response['dates'] = dates

        time_objs = Time.objects.filter(barber_id=barber_id)
        times = [{'id': obj.id, 'time': obj.time.strftime('%H:%M')} for obj in time_objs]
        response['times'] = times

    return JsonResponse(response)




# Tarif yaratish va boshqarish<<<
class LevelManageView(LoginRequiredMixin, View):
    template_name = 'pages/levels_list.html'

    def get(self, request):
        form = LevelForm()
        if request.user.is_superuser:
            levels = Level.objects.all()
        else:
            try:
                barber = Barber.objects.get(user=request.user)
            except Barber.DoesNotExist:
                return redirect('not_barber')
            levels = Level.objects.filter(barber=barber)
        return render(request, self.template_name, {'form': form, 'levels': levels})

    def post(self, request):
        form = LevelForm(request.POST)
        if form.is_valid():
            level = form.save(commit=False)
            level.barber = Barber.objects.get(user=request.user)
            level.save()
            return redirect('level_list')

        if request.user.is_superuser:
            levels = Level.objects.all()
        else:
            levels = Level.objects.filter(barber=request.user)

        return render(request, self.template_name, {'form': form, 'levels': levels})


# Tarifni o'chirish<<<
class LevelDeleteView(LoginRequiredMixin, DeleteView):
    model = Level
    template_name = 'pages/levels_list.html'
    success_url = reverse_lazy('level_list')

    def test_func(self):
        return self.get_object().barber == self.request.user or self.request.user.is_superuser


# Sana va Vaqtlarni boshqarish<<<
@login_required
def manage_schedule_view(request):
    if request.method == 'POST':
        try:
            barber = Barber.objects.get(user=request.user)
        except Barber.DoesNotExist:
            return redirect('not_barber')
        date_form = DateForm(request.POST, barber=barber)
        time_form = TimeForm(request.POST, barber=barber)

        if date_form.is_valid() and time_form.is_valid():
            # === Sana (date) larni saqlash ===
            import datetime
            today = datetime.date.today()
            Date.objects.filter(barber=barber).delete()
            for i in range(30):
                day = today + datetime.timedelta(days=i)
                field_name = f'date_{day}'
                if date_form.cleaned_data.get(field_name):
                    Date.objects.get_or_create(barber=barber, date=day)

            # === Vaqt (time) larni saqlash ===
            Time.objects.filter(barber=barber).delete()
            for field_name, value in time_form.cleaned_data.items():
                if value and field_name.startswith('time_'):
                    time_str = field_name.replace('time_', '')
                    time_obj = datetime.datetime.strptime(time_str, '%H:%M').time()
                    Time.objects.get_or_create(barber=barber, time=time_obj)

            return redirect('manage_schedule')
    else:
        try:
            barber = Barber.objects.get(user=request.user)
        except Barber.DoesNotExist:
            return redirect('not_barber')
        date_form = DateForm(barber=barber)
        time_form = TimeForm(barber=barber)

    return render(request, 'pages/times_dates.html', {
        'date_form': date_form,
        'time_form': time_form
    })


# Barber bilan Tariflarni olish<<<
@login_required
def get_levels_by_barber(request):
    barber_id = request.GET.get('barber_id')  # Bu Barber modelidagi ID
    try:
        barber = Barber.objects.get(id=barber_id)
        user_id = barber.id
        levels = Level.objects.filter(barber_id=user_id).values('id', 'name', 'value')
        return JsonResponse({'levels': list(levels)})
    except Barber.DoesNotExist:
        return JsonResponse({'levels': []}, status=404)


# Barber bilan Sanalarni olish<<<
@login_required
def get_dates_by_barber(request):
    barber_id = request.GET.get('barber_id')  # Bu Barber modelidagi ID
    try:
        barber = Barber.objects.get(id=barber_id)
        user_id = barber.id
        dates = Date.objects.filter(barber_id=user_id).values('id', 'date')
        return JsonResponse({'dates': list(dates)})
    except Barber.DoesNotExist:
        return JsonResponse({'dates': []}, status=404)


# Barber bilan Vaqtlarni olish<<<
@login_required
def get_times_by_barber(request):
    barber_id = request.GET.get('barber_id')
    try:
        barber = Barber.objects.get(id=barber_id)
        user_id = barber.id
        times = Time.objects.filter(barber_id=user_id).values('id', 'time')
        return JsonResponse({'times': list(times)})
    except Barber.DoesNotExist:
        return JsonResponse({'times': []}, status=404)


# Balanceni boshqarish<<<
def account_view(request):
    user = request.user
    form = BalanceForm()
    withdrawals = Balance.objects.filter(user=user).order_by('-date')

    today_total = withdrawals.filter(date__date=timezone.now().date()).aggregate(total=Sum('amount'))['total'] or 0
    week_total = \
        withdrawals.filter(date__gte=timezone.now() - timezone.timedelta(days=7)).aggregate(total=Sum('amount'))[
            'total'] or 0
    month_total = \
        withdrawals.filter(date__gte=timezone.now() - timezone.timedelta(days=30)).aggregate(total=Sum('amount'))[
            'total'] or 0

    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if user.account_balance >= amount:
                user.account_balance -= amount
                user.save()
                Balance.objects.create(user=user, amount=amount)
                messages.success(request, f"{amount} so'm balansdan yechildi.")
                return redirect('balance')
            else:
                messages.error(request, "Balansda yetarli mablag' mavjud emas.")

    return render(request, 'pages/balance.html', {
        'form': form,
        'balance': user.account_balance,
        'withdrawals': withdrawals,
        'today_total': today_total,
        'week_total': week_total,
        'month_total': month_total,
    })


User = get_user_model()


def reset_account_balance(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.account_balance = 0.000
    user.save()

    return redirect('balance')


# Adminlik uchun kod olish<<<
@user_passes_test(lambda u: u.is_superuser)
def staff_codes_page(request):
    codes = StaffCode.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            code = request.POST.get('code')
            if code:
                StaffCode.objects.create(code=code)
                messages.success(request, "Yangi staff code qo‘shildi.")
            return redirect('staffcode-page')

        elif action == 'edit':
            code_id = request.POST.get('code_id')
            code = request.POST.get('code')
            obj = get_object_or_404(StaffCode, pk=code_id)
            obj.code = code
            obj.save()
            messages.success(request, "Staff code yangilandi.")
            return redirect('staffcode-page')

        elif action == 'delete':
            code_id = request.POST.get('code_id')
            obj = get_object_or_404(StaffCode, pk=code_id)
            obj.delete()
            messages.success(request, "Staff code o‘chirildi.")
            return redirect('staffcode-page')

    return render(request, 'pages/staff_code.html', {'codes': codes})
