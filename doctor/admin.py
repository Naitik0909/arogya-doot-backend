from django.contrib import admin

from .models import *

admin.site.register(Doctor)
admin.site.register(Treatment)

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'created_at')