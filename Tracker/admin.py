from django.contrib import admin
from Tracker.models import *
admin.site.site_header="Expense Tracker"
admin.site.site_title="Expense Tracker"
admin.site.site_url="Expense Tracker"

# Register your models here.
admin.site.register(currentbalance)

@admin.action(description="Mark Selected Expenses as Debit")
def make_credit(modeladmin, request, queryset):
    queryset.update(expense_type="CREDIT")


class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display=[
        "amount",
        "current_balance",
        "expense_type",
        "description",
        "created_at"
    ]
    search_fields=['expense_type','description']
    list_filter=['expense_type']
    ordering=['-expense_type']
    actions=[make_credit]
admin.site.register(TrackingHistory, TrackingHistoryAdmin)