# tasks.py
from celery import shared_task
import pandas as pd
from customer.models import Customer
from loan.models import Loan

# @shared_task
def process_excel_data(customer_file_path):
    # Read customer data from Excel
    customer_df = pd.read_excel(customer_file_path)
    for _, row in customer_df.iterrows():
        Customer.objects.create(
        customer_id=row['Customer ID'],  
        first_name=row['First Name'],     
        last_name=row['Last Name'],       
        age=row['Age'],                   
        phone_number=row['Phone Number'], 
        monthly_salary=row['Monthly Salary'],  
        approved_limit=row['Approved Limit'],  
        current_debt=0
    )

    # Read loan data from Excel
    # loan_df = pd.read_excel(loan_file_path)
    # for _, row in loan_df.iterrows():
    #     Loan.objects.create(
    #         customer_id=row['customer_id'],
    #         loan_id=row['loan_id'],
    #         loan_amount=row['loan_amount'],
    #         tenure=row['tenure'],
    #         interest_rate=row['interest_rate'],
    #         monthly_repayment=row['monthly_repayment'],
    #         emis_paid_on_time=row['emis_paid_on_time'],
    #         start_date=row['start_date'],
    #         end_date=row['end_date']
    #     )
