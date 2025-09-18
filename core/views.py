from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer  # Ensure the Customer model is imported
# ... other imports ...

@api_view(['POST'])
def check_eligibility(request):
    customer_id = request.data['customer_id']
    amount = float(request.data['loan_amount'])
    rate = float(request.data['interest_rate'])
    tenure = int(request.data['tenure'])
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response(
            {"error": "Customer with the given ID does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )
    # ...existing code...