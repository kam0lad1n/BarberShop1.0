from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/', ClientsListView.as_view(), name='clients'),
    path('clients/', OnlyClientsRead.as_view(), name='clients_only'),
    # path('barber/clients/<int:barber_id>/', BarberClientsListView.as_view(), name='barber-clients'),
    path('new-site/', booking_view, name='create'),
    path('get-barber-data/', get_data_for_barber, name='get_barber_data'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='delete'),
    path('clients/complete/<int:client_id>/', complete_client, name='complete_client'),

]
