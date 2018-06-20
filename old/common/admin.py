from django.contrib import admin
from common.models import *


class DistilleryAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'still_id']
    search_fields = ['user', 'name']
admin.site.register(Distillery, DistilleryAdmin)


class RunAdmin(admin.ModelAdmin):
    list_display = ['distillery', 'num_data_points', 'start_time', 'end_time']
admin.site.register(Run, RunAdmin)

admin.site.register(Sensor)
admin.site.register(TemperatureDatum)


