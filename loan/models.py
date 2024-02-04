from django.db import models
from customer.models import Customer


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.AutoField(unique=True, primary_key=True)
    loan_amount = models.FloatField(null=True, blank=True)
    tenure = models.IntegerField(null=True, blank=True)
    interest_rate = models.FloatField(null=True, blank=True)
    monthly_repayment = models.FloatField()
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for {self.customer}"
