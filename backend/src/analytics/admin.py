from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('type', 'timestamp')
    fields = ("type", "payload", "timestamp")
    readonly_fields = ('timestamp',)


admin.site.register(Event, EventAdmin)