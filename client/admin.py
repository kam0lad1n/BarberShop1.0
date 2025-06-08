from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    exclude = [ 'owner']
    list_filter = ('barber','level', 'sana')


admin.site.register(Client,ClientAdmin )
admin.site.register(Barber)
admin.site.register(Date )
admin.site.register(Time )
@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'barber')
    list_filter = ('barber',)
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(barber=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.barber != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.barber != request.user:
            return False
        return True
admin.site.register(Balance)
admin.site.register(StaffCode)