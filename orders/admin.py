from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "sample_name",
        "user",
        "sample_type",
        "project_type",
        "status",
        "created_at",
    )
    list_filter = ("project_type", "status", "created_at")
    list_editable = ("status",)
    search_fields = ("sample_name", "sample_type", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
