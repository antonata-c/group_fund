from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Collect, Payment


class CollectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'reason',
        'planned_amount', 'current_amount', 'end_date'
    )
    list_filter = ('reason', 'end_date')
    search_fields = ('title', 'description')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'collect', 'amount', 'created_at', 'hide_amount')
    list_filter = ('created_at', 'hide_amount')


admin.site.unregister(Group)
admin.site.register(Collect, CollectAdmin)
admin.site.register(Payment, PaymentAdmin)
