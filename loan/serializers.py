from rest_framework import serializers
from customer.serializers import CustomerSerializer
from .models import Loan
from customer.models import Customer


class LoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = "__all__"


class LoanDetailCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "phone_number", "age"]


class SingleLoanDetailSerializer(serializers.ModelSerializer):
    customer = LoanDetailCustomerSerializer(source="customer_data", read_only=True)
    monthly_installment = serializers.FloatField(source="monthly_repayment")

    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "customer",
            "loan_amount",
            "interest_rate",
            "tenure",
            "monthly_installment",
        ]


class CreateLoanRequestSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class CreateLoanResponseSerializer(serializers.Serializer):
    loan_id = serializers.IntegerField(required=False, allow_null=True)
    customer_id = serializers.IntegerField()
    loan_approved = serializers.BooleanField()
    message = serializers.CharField(required=False, allow_blank=True)
    monthly_installment = serializers.FloatField(required=False, allow_null=True)


class LoanEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()


class LoanDetailSerializer(serializers.ModelSerializer):
    monthly_installment = serializers.FloatField(source="monthly_repayment")
    repayments_left = serializers.SerializerMethodField(
        method_name="get_repayments_left"
    )

    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "loan_amount",
            "interest_rate",
            "monthly_installment",
            "repayments_left",
        ]

    def get_repayments_left(self, obj: Loan):
        return obj.tenure - obj.emis_paid_on_time
