from django.contrib import admin

# Register your models here.
class GatewayAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "active",
    )
