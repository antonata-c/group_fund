from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    Collect,
    EmailTemplate,
    Payment
)


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "reason", "amount", "end_date")
    list_filter = ("reason", "end_date")
    search_fields = ("title", "description")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "collect", "amount", "created_at", "hide_amount")
    list_filter = ("created_at", "hide_amount")


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "is_html")


admin.site.unregister(Group)
