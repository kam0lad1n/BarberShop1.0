from django.urls import path
from client.views import *
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin_view, name='admin'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/site/update/', site_update, name='site_update'),
    path('profile/barber/barbers/', BarberCreateView.as_view(), name='add_barber'),
    path('profile/sites/<int:pk>/delete/', DeleteBarbers.as_view(), name='delete_barber'),
    path('not_barber/', not_barber, name='not_barber'),
    path('profile/manage-schedule/', manage_schedule_view, name='manage_schedule'),
    path('profile/users/', users_list, name='users_list'),
    path('profile/make-admin/<int:user_id>/', make_admin, name='make_admin'),
    path('profile/remove-admin/<int:user_id>/', remove_admin, name='remove_admin'),
    path('profile/users/delete/<int:user_id>/', delete_user, name='remove_user'),
    path('profile/levels/', LevelManageView.as_view(), name='level_list'),
    path('profile/levels/delete/<int:pk>/', LevelDeleteView.as_view(), name='delete_level'),

    path('ajax/levels/', get_levels_by_barber, name='ajax_levels'),
    path('ajax/dates/', get_dates_by_barber, name='ajax_dates'),
    path('ajax/times/', get_times_by_barber, name='ajax_times'),
    path('profile/balance/', account_view, name='balance'),
    path('profile/reset_balance/<int:user_id>/', reset_account_balance, name='reset_balance'),
    path('profile/staff-codes/', staff_codes_page, name='staffcode-page'),

]
