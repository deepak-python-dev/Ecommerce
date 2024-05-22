from django.contrib import admin
from .models import CustomUser, Order

class CustomUserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CustomUser._meta.fields]

class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Order, OrderAdmin)