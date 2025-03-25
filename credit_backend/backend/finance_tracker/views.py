from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.models import User  # ✅ Import User model from Cred-It
from backend.finance_tracker.models import Transaction
from backend.finance_tracker.serializers import TransactionSerializer
from backend.finance_tracker.forms import TransactionForm
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(f"Request User: {self.request.user}")  # Debugging
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print(f"Saving transaction for: {self.request.user}")  # Debugging
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])  # ✅ Require authentication from Cred-It
def get_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_filtered_transactions(request):
    filter_type = request.GET.get("filter", "all")  
    today = datetime.today().date()

    if filter_type == "daily":
        start_date, end_date = today, today
    elif filter_type == "weekly":
        start_date = today - timedelta(days=today.weekday())  
        end_date = start_date + timedelta(days=6)
    elif filter_type == "monthly":
        start_date = today.replace(day=1)
        next_month = today.replace(day=28) + timedelta(days=4)  
        end_date = next_month - timedelta(days=next_month.day)
    elif filter_type == "yearly":
        start_date, end_date = today.replace(month=1, day=1), today.replace(month=12, day=31)
    else:
        start_date, end_date = None, None  

    transactions = Transaction.objects.filter(user=request.user)
    
    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)
