from django.contrib import admin
from .models import Tariff, Subscription

@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tariff', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'tariff', 'start_date')
    search_fields = ('user__username', 'user__email')
