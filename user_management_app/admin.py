from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time']


@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_type', 'duration', 'price']



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_price', 'slot', 'booking_date', 'status', 'representative']