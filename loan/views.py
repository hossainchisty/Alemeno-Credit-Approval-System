import datetime
from django.db import transaction
from dateutil.relativedelta import relativedelta
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Loan
from customer.models import Customer
from .serializers import (
    CreateLoanResponseSerializer,
    LoanEligibilitySerializer,
    CreateLoanRequestSerializer,
    SingleLoanDetailSerializer,
    LoanDetailSerializer,
)
from .utils import (
    check_eligibility,
    calculate_credit_score,
    calculate_remaining_loan_balance,
)
import numpy_financial as npf
from django.core.exceptions import ObjectDoesNotExist


class ViewLoansView(APIView):
    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            loans = Loan.objects.filter(
                customer_id=customer_id, end_date__gte=datetime.date.today()
            )
            serializer = LoanDetailSerializer(loans, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response(
                {"message": "Customer not found."}, status=status.HTTP_400_BAD_REQUEST
            )


class ViewLoanView(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.filter(loan_id=loan_id).first()
            loan.customer_data = Customer.objects.get(customer_id=loan.customer_id)
            serializer = SingleLoanDetailSerializer(instance=loan)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response(
                {"message": "Loan not found."}, status=status.HTTP_400_BAD_REQUEST
            )


class CreateLoanView(APIView):
    def post(self, request):
        serializer = CreateLoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = serializer.validated_data["customer_id"]
            loan_amount = serializer.validated_data["loan_amount"]
            interest_rate = serializer.validated_data["interest_rate"]
            tenure = serializer.validated_data["tenure"]

            customer = Customer.objects.get(customer_id=customer_id)
            loans = Loan.objects.filter(customer=customer)

            credit_score = calculate_credit_score(loans=loans, customer=customer)

            loan_approved, corrected_interest_rate = check_eligibility(
                credit_score=credit_score,
                interest_rate=interest_rate,
                customer=customer,
                loans=loans,
            )
            message = (
                "Loan approved by authority" if loan_approved else "Loan not approved"
            )
            monthly_installment = npf.pmt(
                rate=interest_rate / 12, nper=tenure, pv=-loan_amount
            )

            start_date = datetime.datetime.today().date()

            end_date = start_date + relativedelta(months=+tenure)

            if loan_approved:
                with transaction.atomic():
                    loan = Loan.objects.create(
                        customer=customer,
                        loan_amount=loan_amount,
                        interest_rate=corrected_interest_rate,
                        tenure=tenure,
                        start_date=start_date,
                        end_date=end_date,
                        emis_paid_on_time=0,
                        monthly_repayment=monthly_installment,
                    )
                    loan_id = loan.loan_id
                    customer.customer_id += calculate_remaining_loan_balance(loan)
                    customer.save()

                response_data = {
                    "loan_id": loan_id,
                    "customer_id": customer_id,
                    "loan_approved": loan_approved,
                    "message": message,
                    "monthly_installment": monthly_installment,
                }

            else:
                response_data = {
                    "loan_id": None,
                    "customer_id": customer_id,
                    "loan_approved": loan_approved,
                    "message": message,
                    "monthly_installment": None,
                }
            response_serializer = CreateLoanResponseSerializer(data=response_data)
            print(response_serializer)
            if response_serializer.is_valid():
                return Response(
                    response_serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                response_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckEligibilityView(APIView):
    def get(self, request):
        serializer = LoanEligibilitySerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve customer and loan data
            customer_id = serializer.validated_data["customer_id"]
            customer = Customer.objects.get(customer_id=customer_id)
            loans = Loan.objects.filter(customer_id=customer_id)
            loan_amount = serializer.validated_data["loan_amount"]
            interest_rate = serializer.validated_data["interest_rate"]
            tenure = serializer.validated_data["tenure"]

            # Calculate credit score for the customer
            credit_score = calculate_credit_score(loans=loans, customer=customer)

            # Determine loan approval and interest rates
            approval, corrected_interest_rate = check_eligibility(
                credit_score=credit_score,
                interest_rate=interest_rate,
                customer=customer,
                loans=loans,
            )

            # Calculate monthly installment if approved
            if approval:
                monthly_installment = npf.pmt(
                    rate=interest_rate / 12, nper=tenure, pv=-loan_amount
                )
            else:
                monthly_installment = 0

            response_data = {
                "customer_id": customer_id,
                "approval": approval,
                "interest_rate": interest_rate,
                "corrected_interest_rate": corrected_interest_rate,
                "tenure": tenure,
                "monthly_installment": monthly_installment,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
