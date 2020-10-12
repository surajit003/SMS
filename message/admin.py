from django.contrib import admin
from message.models import Gateway, Message

# Register your models here.
@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "configured_sender",
        "active",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "partner_message_id",
        "status",
        "recipient",
    )
    search_fields = ("partner_message_id", "recipient")
