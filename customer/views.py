from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from customer.models import Customer

class CustomerRegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            approved_limit = round(36 * data['monthly_income'], -5)  # Rounded to nearest lakh
            customer = Customer.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                age=data['age'],
                monthly_salary=data['monthly_income'],
                approved_limit=approved_limit,
                current_debt=0
            )
            return Response({
                'customer_id': customer.customer_id,
                'name': f"{customer.first_name} {customer.last_name}",
                'age': data['age'],
                'monthly_income': data['monthly_income'],
                'approved_limit': approved_limit,
                'phone_number': data['phone_number']
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

