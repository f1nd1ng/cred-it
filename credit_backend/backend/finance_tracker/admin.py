from django.contrib import admin
from backend.finance_tracker.models import Transaction

# ✅ Check if Transaction is already registered before registering
if not admin.site.is_registered(Transaction):
    @admin.register(Transaction)
    class TransactionAdmin(admin.ModelAdmin):
        list_display = ("user", "category", "amount", "currency", "date")
        list_filter = ("category", "transaction_type", "date")
        search_fields = ("user__email", "category", "description")
