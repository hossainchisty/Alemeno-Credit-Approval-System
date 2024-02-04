from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from customer.models import Customer
from loan.models import Loan

import time
class DataInsertView(APIView):

    def get(self, request):
        start_time = time.time()
        customer_df = pd.read_excel(r'C:\Users\USER OS\Desktop\credit_approval_system\customer_data.xlsx')
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
        loan_df = pd.read_excel(r'C:\Users\USER OS\Desktop\credit_approval_system\loan_data.xlsx')
        for _, row in loan_df.iterrows():
            Loan.objects.create(
                customer_id=row['Customer ID'],
                loan_id=row['Loan ID'],         
                loan_amount=row['Loan Amount'], 
                tenure=row['Tenure'],           
                interest_rate=row['Interest Rate'],
                monthly_repayment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=row['Date of Approval'],   
                end_date=row['End Date']        
            )
        # process_excel_data.delay(r'C:\Users\USER OS\Desktop\credit_approval_system\customer_data.xlsx')
        # '
        end_time = time.time()
        execution_time = end_time - start_time

        print("Execution time:", execution_time, "seconds")
        return Response({'message': 'Data processing task has been queued.', 'Excution Time': execution_time })