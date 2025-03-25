from rest_framework import serializers
from backend.finance_tracker.models import Transaction
from backend.models import User  # ✅ Import Cred-It User Model

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # ✅ Ensure the user is from Cred-It

    class Meta:
        model = Transaction
        fields = "__all__"
