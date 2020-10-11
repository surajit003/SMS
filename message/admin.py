from django.contrib import admin
from message.models import Gateway

# Register your models here.
@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "configured_sender",
        "active",
    )
