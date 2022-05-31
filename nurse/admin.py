from django.contrib import admin
from .models import *

admin.site.register(Bed)

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    empty_value_display = 'N/A'
    list_display = ('__str__', 'id', 'phone')
    ordering=('user__first_name', 'user__last_name')
    list_filter = ('is_day_shift', )
    # search_fields = ['user__username', 'user__first_name', '__str__']
