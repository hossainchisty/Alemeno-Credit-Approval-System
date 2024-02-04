from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    monthly_salary = models.FloatField()
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(null=True, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
