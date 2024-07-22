from django.contrib import admin
from .models import Membres
# Register your models here.

class DashMembres(admin.ModelAdmin):
    list_display = ("Pseudo","email","photo","pwd")
    search_fields = ("Pseudo","email")

admin.site.register(Membres, DashMembres)