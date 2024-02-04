import datetime
import numpy_financial as npf
from django.db.models import QuerySet
from .models import Loan
from customer.models import Customer

def calculate_remaining_loan_balance(loan):
    monthly_interest_rate = loan.interest_rate / 12 / 100

    # Calculate the number of payments already made
    payments_made = loan.emis_paid_on_time

    # The remaining balance is the future value of the remaining payments
    remaining_balance = npf.fv(rate=monthly_interest_rate, nper=loan.tenure - payments_made, pmt=-loan.monthly_repayment, pv=loan.loan_amount, when='end')

    return abs(remaining_balance)

def calculate_credit_score(loans: QuerySet[Loan], customer: Customer) -> int:
    current_year = datetime.datetime.now().year
    number_of_past_loans = loans.count()
    loan_activity_current_year = 0
    loan_approved_volume = 0
    total_emis_paid_on_time = 0
    total_emis_tenure = 0

    max_loan_amount = max([loan.loan_amount for loan in loans])
    for loan in loans:
        total_emis_paid_on_time += loan.emis_paid_on_time
        total_emis_tenure += loan.tenure
        if loan.start_date.year == current_year:
            loan_activity_current_year += 1
        loan_approved_volume += loan.loan_amount / max_loan_amount

    past_loans_paid_on_time = total_emis_paid_on_time / total_emis_tenure

    # Initial credit score calculation
    credit_score = 0
    credit_score += past_loans_paid_on_time * 25
    credit_score += number_of_past_loans * 25
    credit_score += loan_activity_current_year * 25
    credit_score += float(loan_approved_volume * 25)

    if customer.current_debt > customer.approved_limit:
        credit_score = 0
    return credit_score

def check_eligibility(credit_score: float, interest_rate: float, customer: Customer, loans: QuerySet[Loan]):
    monthly_salary = customer.monthly_salary
    total_emi = sum(loan.monthly_repayment for loan in loans if loan.end_date > datetime.date.today())
    approval = False
    corrected_interest_rate = interest_rate
    if total_emi > float(monthly_salary) * 0.5:
        approval = False
    elif credit_score > 50:
        approval = True
    elif 50 > credit_score > 30:
        approval = True
        corrected_interest_rate = max(interest_rate, 12)
    elif 30 > credit_score > 10:
        approval = True
        corrected_interest_rate = max(interest_rate, 16)
    return approval, corrected_interest_rate

