from rest_framework import serializers
from .models import Customer
class RegisterSerializer(serializers.ModelSerializer):
    monthly_income = serializers.FloatField()

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'monthly_income', 'phone_number']
        
        
        
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
