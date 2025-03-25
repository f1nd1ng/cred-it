from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.finance_tracker.views import (
    TransactionViewSet,
    transaction_list,
    transaction_create,
    get_filtered_transactions
)

# ✅ Router for API endpoints
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', transaction_list, name='transaction_list'),  # ✅ finance_tracker/ (List Transactions)
    path('create/', transaction_create, name='transaction_create'),  # ✅ finance_tracker/create/ (Add Transaction)
    path('api/transactions/filter/', get_filtered_transactions, name="filtered_transactions"),  # ✅ finance_tracker/filter/ ->for frontend
    
    # ✅ Include API routes under finance_tracker/api/
    path('api/', include(router.urls)),  
]
